from datetime import date

from fastapi import APIRouter
from fastapi import Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi import responses

from db_queries import get_ant_by_id
from model.session import get_db
from model.ant_input import Color, AntInput
from prediction import predict_label


templates = Jinja2Templates(directory="templates")
general_pages_router = APIRouter()


@general_pages_router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("form.html", {"request":request})


@general_pages_router.post('/')
def form_post(thorax_color: Color = Form(),
              paunch_color: Color = Form(),
              length: int = Form(),
              finding_date: date = Form(),
              ant_image = Form()):
    ant_info = AntInput(thorax_color=thorax_color, paunch_color=paunch_color, length=length, finding_date=finding_date)
    label = predict_label(ant_image, ant_info)
    return responses.RedirectResponse('/ants_pred/' + str(label))


@general_pages_router.post("/ants_pred/{id}")
async def get_ant(request: Request, id: int, session=Depends(get_db)):
    result = get_ant_by_id(id, db=session)
    description = result.description
    name = result.name
    image_path = '/static/predictions/predict.jpg'
    return templates.TemplateResponse('show_ant.html', context={'request': request,
                                                                'description': description,
                                                                'name': name,
                                                                'image': image_path})


@general_pages_router.get("/ants/{id}")
async def get_ant(request: Request, id: int, session=Depends(get_db)):
    result = get_ant_by_id(id, db=session)
    description = result.description
    name = result.name
    return templates.TemplateResponse('show_ant.html', context={'request': request,
                                                                'description': description,
                                                                'name': name})