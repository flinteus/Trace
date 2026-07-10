import os
import aiofiles
import re
from typing import Optional, Tuple
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import select

from app.schemas.log import LogQueryParams, LogResponse, LogEntry
from app.models.agent import Agent

# Константы (можно вынести в config)
ALLOWED_LOG_PATHS = [
    "/var/log",
    "/tmp/test-logs", 
]
MAX_LOG_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

def _validate_log_path(log_name: str, base_path: str = "/var/log") -> str:
    """Валидация пути лога (защита от directory traversal)."""
    full_path = os.path.normpath(os.path.join(base_path, log_name))
    
    is_allowed = any(
        os.path.commonpath([full_path, allowed]) == allowed
        for allowed in ALLOWED_LOG_PATHS
    )
    
    if not is_allowed:
        raise HTTPException(
            status_code=403,
            detail="Access to this log file is forbidden"
        )
    return full_path

def _parse_log_line(line: str) -> Tuple[Optional[datetime], Optional[str]]:
    """Извлекает timestamp и уровень из строки лога."""
    timestamp = None
    level = None
    
    ts_match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)
    if ts_match:
        try:
            timestamp = datetime.strptime(ts_match.group(), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass
    
    lvl_match = re.search(r'\b(INFO|WARNING|ERROR|DEBUG|CRITICAL)\b', line, re.IGNORECASE)
    if lvl_match:
        level = lvl_match.group().upper()
    
    return timestamp, level

async def read_log(
    log_name: str,
    params: LogQueryParams,
    agent_base_path: str = "/var/log",
) -> LogResponse:
    """
    Асинхронно читает лог-файл с пагинацией и поиском.
    
    Args:
        log_name: Имя файла лога
        params: Параметры запроса (лимит, смещение, поиск)
        agent_base_path: Базовая директория логов агента
        
    Returns:
        LogResponse: Структурированный ответ
    """
    log_path = _validate_log_path(log_name, agent_base_path)
    
    if not os.path.exists(log_path):
        raise HTTPException(404, f"Log file '{log_name}' not found")
    
    file_size = os.path.getsize(log_path)
    if file_size > MAX_LOG_FILE_SIZE:
        raise HTTPException(
            413,
            f"Log file too large ({file_size / 1024 / 1024:.1f} MB)"
        )
    
    try:
        async with aiofiles.open(log_path, 'r', encoding='utf-8') as f:
            if params.offset > 0:
                await f.seek(params.offset)
            
            lines = []
            buffer_size = 8192
            buffer = ""
            
            while len(lines) < params.lines:
                chunk = await f.read(buffer_size)
                if not chunk:
                    break
                buffer += chunk
                while '\n' in buffer and len(lines) < params.lines:
                    line, buffer = buffer.split('\n', 1)
                    lines.append(line)
            
            if buffer and len(lines) < params.lines:
                lines.append(buffer)
            
            if params.search:
                lines = [line for line in lines if params.search.lower() in line.lower()]
            
            entries = [
                LogEntry(
                    line_number=idx + 1,
                    content=line,
                    timestamp=_parse_log_line(line)[0],
                    level=_parse_log_line(line)[1],
                )
                for idx, line in enumerate(lines)
            ]
            
            current_pos = await f.tell()
            has_more = current_pos < file_size
            
            return LogResponse(
                log_name=log_name,
                total_lines=None,  
                returned_lines=len(entries),
                entries=entries,
                has_more=has_more,
                next_offset=current_pos if has_more else None,
            )
            
    except UnicodeDecodeError:
        raise HTTPException(400, "Log file is not UTF-8 encoded")
    except PermissionError:
        raise HTTPException(403, "Permission denied")
    except Exception as e:
        raise HTTPException(500, f"Error reading log: {str(e)}")


async def get_logfile(
        db: AsyncSession,
        user_id: str,
        agent_id: str,
        params: LogQueryParams,
        agent_base_path: str = "/var/log",
) -> list[LogResponse]:
    
    stmt = select(Agent).where(
        Agent.id == agent_id,
        Agent.user_id == user_id
    )
    result = await db.execute(stmt)
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found or access denied"
        )        
    
    async with aiofiles.open(agent_base_path, 'r', encoding='utf-8') as f:
            if params.offset > 0:
                await f.seek(params.offset)    

            result = [x for x in f]

            # return LogResponse(
            #     log_name=log_name,
            #     total_lines=None,  
            #     returned_lines=len(entries),
            #     entries=entries,
            #     has_more=has_more,
            #     next_offset=current_pos if has_more else None,
            # )
            
            #TODO: доделать эндромнт


