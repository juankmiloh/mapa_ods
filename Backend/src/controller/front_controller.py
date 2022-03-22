from flask import render_template, request
from ..controller import controller
from ..util.constants import API_ROOT_PATH 


@controller.route('', methods=['GET'], defaults={'path': ''})
def home(path):
    script_root  = request.script_root
    
    if script_root :
        script_root += "/"

    return render_template("dist/index.html", url_base=script_root + "ods/front/dist")

@controller.route('/map-page', methods=['GET'], defaults={'path': ''})
def home_api(path):
    script_root  = request.script_root
    
    if script_root :
        script_root += "/"

    return render_template("dist/index.html", url_base=script_root + "ods/front/dist" )

@controller.route('front/dist/', methods=['GET'], defaults={'path': ''})
def home_apiv1(path):
    script_root  = request.script_root
    
    if script_root :
        script_root += "/"

    return render_template("dist/index.html", url_base=script_root + "ods/front/dist" )

@controller.route('ods/front/dist/', methods=['GET'], defaults={'path': ''})
def home_apiv2(path):
    script_root  = request.script_root
    
    if script_root :
        script_root += "/"

    return render_template("dist/index.html", url_base=script_root + "ods/front/dist" )

@controller.route('ods/', methods=['GET'], defaults={'path': ''})
def home_apiv3(path):
    script_root  = request.script_root
    
    if script_root :
        script_root += "/"

    return render_template("dist/index.html", url_base=script_root + "ods/front/dist" )

@controller.route('front/dist/map-page', methods=['GET'], defaults={'path': ''})
def home_apiv4(path):
    script_root  = request.script_root
    
    if script_root :
        script_root += "/"

    return render_template("dist/index.html", url_base=script_root + "ods/front/dist" )
