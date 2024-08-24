import os

import urllib.request

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models.models import file, User
from tasks.tasks import save_file
from auth.base_config import current_user

router = APIRouter(
    prefix='/files',
    tags=['files']
)

@router.get('/')
async def get_files(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Получение информации о загруженных файлах из БД"""
    query = select(file).where(file.c.author_id == user.id)
    result = await session.execute(query)
    res = result.mappings().all()
    return res


@router.get('/{file_id}')
async def get_file(
        file_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Получение информации о загруженном файле по его ID"""
    query = select(file).where(
        file.c.id == file_id, file.c.author_id == user.id)
    result = await session.execute(query)
    file_info = result.mappings().first()

    if file_info is None:
        raise HTTPException(status_code=404, detail="Файл не найден")

    return file_info


@router.delete('/{file_id}')
async def delete_file(
        file_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Удаление файла и его записи из БД по ID"""
    query = select(file).where(
        file.c.id == file_id, file.c.author_id == user.id)
    result = await session.execute(query)
    file_info = result.mappings().first()

    if file_info is None:
        raise HTTPException(status_code=404, detail="Файл не найден")

    file_path = file_info['link_download']

    # Удаляем запись о файле из БД
    delete_query = file.delete().where(file.c.id == file_id)
    await session.execute(delete_query)
    await session.commit()

    # Удаляем физический файл с сервера
    try:
        os.remove(file_path)
    except OSError as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при удалении файла: {str(e)}")

    return {"detail": "Файл успешно удалён"}


@router.post('/')
async def upload_file(
        link: str,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """
        Эндпоинт для загрузки файла по переданной ссылке.
        Пример ссылки для загрузки файла\n
        https://psv4.userapi.com/c537232/u11445139/docs/d15/e6c5ae13869b/Nissan_Almera_N16_Manual_rus.pdf?extra=ZThmAb_9cdSH3hqTDZ50A07fqV8VKkJEK7aduTGYKB0ClhTRj8i9hNNSOo-RGD43XEQOsTmVFGKuAV5kTfqSKHqEAnYT1FuXErVOo9Ws9IPzpUcEkNSSxuFTBQ5U17OwOf8AFLbeZpQVodo5Z4-dpA&dl=1
    """
    with urllib.request.urlopen(link) as response:
        file_name = os.path.basename(response.geturl()).split("?")[0]
        download_dir = os.path.join(os.getcwd(), 'Download')
        save_path = os.path.join(download_dir, file_name)
        if os.path.exists(save_path):
            return {"message": "Такой файл уже существует!"}
        else:
            save_file.delay(link)

        stmt = insert(file).values(
            name=file_name, link_download=save_path, author_id=user.id)
        await session.execute(stmt)
        await session.commit()

    return {"status": "success"}


@router.get("/download/{file_id}")
async def download_file(
        file_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """
    Эндпоинт для скачивания файла с сервера.
    """
    query = select(file).where(
        file.c.id == file_id, file.c.author_id == user.id)
    result = await session.execute(query)
    file_info = result.mappings().first()
    file_path = file_info['link_download']

    if not os.path.exists(file_path):
        return {"message": "Файл не найден"}

    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=file_info['name']
    )
