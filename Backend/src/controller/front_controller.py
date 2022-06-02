from flask import render_template, request
from ..controller import controller
from ..util.constants import API_ROOT_PATH


@controller.route('', methods=['GET'], defaults={'path': ''})
def home(path):
    script_root  = request.script_root
    print("--------- roooot ---------------------------")
    print(script_root)
    print("------------------------------------")
    
    if script_root :
        script_root += "/"

    return render_template("index.html", url_base=script_root + "ods/front/dist")

@controller.route('/static/<string:shortcode>')
def shortcode_redirect(shortcode):
    print("--------- shortcode ---------------------------")
    print(shortcode)
    print("------------------------------------")
    return render_template("index.html")

# @controller.route('/map-page', methods=['GET'], defaults={'path': ''})
# def home_api(path):
#     script_root  = request.script_root
    
#     if script_root :
#         script_root += "/"

#     return render_template("dist/index.html", url_base=script_root + "ods/front/dist" )
