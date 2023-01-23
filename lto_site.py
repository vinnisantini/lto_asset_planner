from flask import Flask, render_template, send_file, request
import app_logic as al

# setting up flask application
app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route("/")
def home():
    info = al.return_everything()

    if type(info[1]) == str:
        return render_template('home_page.html', data=[[], [], [], [], [], []])
    else:
        return render_template('home_page.html', data=info)

@app.route("/timeline", methods = ['POST'])
def graph_page():
    info = al.return_everything()
    if request.method == 'POST':
        btn = request.form.get('btn sub')

    if btn == 'assets':
        return show_assets_page()
    else:
        if btn == 'event':
            graphJSON = al.create_event_timeline()
        else:
            graphJSON = al.create_movement_timeline()
        
        return render_template('graph.html', data=info, graphJSON=graphJSON)

@app.route('/create_event', methods = ['POST'])
def create_event():
    if request.method == 'POST':
        name = request.form.get('event')
        sd = request.form.get('sd')
        ed = request.form.get('ed')
    
    al.create_event(name, sd, ed)
    return home()

@app.route('/create_mvmt', methods = ['POST'])
def create_mvmt():
    if request.method == 'POST':
        mv = request.form.getlist('mvmt_type')
        cs = request.form.getlist('cs')
        ol = request.form.getlist('ol')
        dn = request.form.getlist('dn')
        sd = request.form.getlist('sd')
        ed = request.form.getlist('ed')
        start_t = request.form.getlist('start_t')
        end_t = request.form.getlist('end_t')

    al.create_movement(mvmt_type=mv, callsign=cs, org=ol, dest=dn, start=sd, start_time=start_t, end=ed, end_time=end_t)
    return home()

@app.route("/get_lto_dropdown", methods = ['POST'])
def get_lto_dropdown():
    if request.method == 'POST':
        ev = request.form.get('event')
        al.current_lto(ev)

    return home()

@app.route("/get_lto_timeline", methods = ['POST'])
def get_lto_timeline():
    if request.method == 'POST':
        ev = request.form.get('event')
        al.current_lto(ev)

    return graph_page()

@app.route("/show_assets_page")
def show_assets_page():
    info = al.return_everything()
    return render_template('assets.html', data=info)

@app.route("/create_asset", methods = ['POST'])
def create_asset():
    if request.method == 'POST':
        sn = request.form.getlist('sn')
        mak = request.form.getlist('vmak')
        model = request.form.getlist('vmod')
    al.create_assets(serial=sn, make=mak, model=model)

    return show_assets_page()

@app.route('/mvmt_type', methods = ['POST'])
def create_mvmt_type():
    if request.method == 'POST':
        val = request.form.get('mvmt_type')

        al.create_mvmt_type(val)
        
    return show_assets_page()

@app.route('/driver', methods = ['POST'])
def create_driver():
    if request.method == 'POST':
        val = request.form.get('driver_name')

        al.create_driver(val)
        
    return show_assets_page()

if __name__ == '__main__':
    app.run()