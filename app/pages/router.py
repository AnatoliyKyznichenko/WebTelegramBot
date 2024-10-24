from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from app.api.dao import ApplicationDAO, UserDAO
from app.core.config import settings

router_pages = APIRouter(prefix='', tags=['Фронтенд'])
templates = Jinja2Templates(directory='app/templates')


@router_pages.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request, "title": "Элегантная парикмахерская"})


@router_pages.get("/admin", response_class=HTMLResponse)
async def read_root(request: Request, admin_id: int = None):
    data_page = {"request": request, "access": False, 'title_h1': "Панель администратора"}
    if admin_id is None or admin_id != settings.ADMIN_ID:
        data_page['message'] = 'У вас нет прав для получения информации о заявках!'
        return templates.TemplateResponse("applications.html", data_page)
    else:
        data_page['access'] = True
        data_page['applications'] = await ApplicationDAO.get_all_applications()
        return templates.TemplateResponse("applications.html", data_page)


@router_pages.get("/applications", response_class=HTMLResponse)
async def read_root(request: Request, user_id: int = None):
    data_page = {"request": request, "access": False, 'title_h1': "Мои записи"}
    user_check = await UserDAO.find_one_or_none(telegram_id=user_id)

    if user_id is None or user_check is None:
        data_page['message'] = 'Пользователь, по которому нужно отобразить заявки, не указан или не найден в базе данных'
        return templates.TemplateResponse("applications.html", data_page)
    else:
        applications = await ApplicationDAO.get_applications_by_user(user_id=user_id)
        data_page['access'] = True
        if len(applications):
            data_page['applications'] = await ApplicationDAO.get_applications_by_user(user_id=user_id)
            return templates.TemplateResponse("applications.html", data_page)
        else:
            data_page['message'] = 'У вас нет заявок!'
            return templates.TemplateResponse("applications.html", data_page)