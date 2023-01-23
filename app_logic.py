import mysql.connector
import pandas as pd
import plotly
import plotly.express as px
from datetime import datetime
import json

def check_db_connection():
    # CHECKING CONNECTION TO DATABASE
    mydb = mysql.connector.connect(host = "localhost", user = "root", password = "rootpass", database = "lto_planner")

    if mydb.is_connected():
        print('\nis connected\n')
        cur = mydb.cursor()
    else:
        print('\nis not connected creating connection\n')
        mydb = mysql.connector.connect(host = "localhost", user = "root", password = "rootpass", database = "lto_planner")
        cur = mydb.cursor()
    
    return mydb, cur

# CREATING EVENT/NEW LTO
def create_event(name, sd, ed):
    mydb, cur = check_db_connection()
    final_info = f'Created Event: {name} taking place from {ed} to {ed}\n'

    sql_q = "INSERT INTO events (event_name, start_d, end_d) VALUES (%s, %s, %s)"
    info = (name, sd, ed)
    cur.execute(sql_q, info)
    mydb.commit()
    mydb.close()
    print('\ncommited successfully\n')
    return final_info

def create_movement(**ev_info):
    mydb, cur = check_db_connection()
    # grabbing id with event name from database
    cur.execute("SELECT * FROM current_lto")
    lto = cur.fetchall()
    v = lto[0][1]

    sql_q = """INSERT INTO movements (event_id, mvmt_type, call_sign, orgin, destination, start_dt, end_dt) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    
    values = pd.DataFrame.from_dict(ev_info)
    values['start'] = values['start'] + ' '+ values['start_time']
    values['end'] = values['end'] + ' ' +  values['end_time']
    del values['start_time']
    del values['end_time']
    e = values.values.tolist()

    f = [v]

    for i in e:
        f.extend(i)
        print(f)
        cur.execute(sql_q, f)
        mydb.commit()
        print('submmited to database successfuly')

        f.clear()
        f = [v]

    mydb.close()
    return ev_info

def create_assets(**asset_info):
    mydb, cur = check_db_connection()
    assets = pd.DataFrame.from_dict(asset_info)
    asset = assets.values.tolist()

    sql_q = """INSERT INTO assets (serial_num, make, model) VALUES
            (%s, %s, %s)"""
    
    for ass in asset:
        cur.execute(sql_q, ass)
        mydb.commit()
        print('\ncommited successfully\n')
    mydb.close()
    return asset_info

def manage_assets():
    mydb, cur = check_db_connection()
    while True:
        # grabbing id with call_sign name from database
        mvmt = input('\nWhich Event do you want to Manage? (CALL SIGN): ')
        s = "SELECT * FROM movements WHERE call_sign = %s"
        e = (mvmt, )
        cur.execute(s, e)
        mvmt_id = cur.fetchone()[0]

        dn = input('\nEnter Driver Name: ')
        vc = input('Enter VC Name: ')
        sn = input('Enter Vehicle Serial Number used on this Mission: ')
        status = input('Enter Mission Status: ')

        r = "SELECT * FROM assets WHERE serial_num = %s"
        v = (sn, )
        cur.execute(r, v)
        res = cur.fetchone()
        vic = (res[0], f'{res[2]} {res[3]}')

        print(f'Mission {mvmt}: will be supported with {vic}, driver is {dn}, vc is {vc}, current status is {status}')
    
        sql_q = """INSERT INTO management (mvmt_num, driver_name, vc_name, asset_id, status)
                VALUES (%s, %s, %s, %s, %s)"""
            
        info = (mvmt_id, dn, vc, res[0], status)

        cur.execute(sql_q, info)
        mydb.commit()
        mydb.close()
        print('\nCOMMIT SUCCESSFUL\n')

        ex = input('\nFinish Entering Movements? (Y/N): ').upper()

        if ex == 'Y':
            break
        elif ex == 'N':
            continue
        else:
            print('Enter Valid Response')

    return info

def return_everything():
    mydb, cur = check_db_connection()
    mvmts, event_list, l, ass_list, mvmt_types, drivers = 0, 0, 0, 0, 0, 0
    cur.execute("SELECT * FROM events")
    event_list = cur.fetchall()
    
    cur.execute("SELECT * FROM current_lto")
    lto = cur.fetchall()

    if len(event_list) == 0:
        l='0'
        v=0
    else:
        if len(lto) == 0:
            l = 0
            v = 0
        else:
            sql_q = "SELECT * FROM events WHERE e_id = %s"
            v = lto[0][1]
            cur.execute(sql_q, [v,])
            l = cur.fetchone()

    cur.execute("SELECT * FROM mvmt_types")
    mvmt_types = cur.fetchall()

    cur.execute("SELECT * FROM drivers")
    drivers = cur.fetchall()

    # gathering and filtering all the information for the movements
    fil_mvmt = "SELECT * FROM movements WHERE event_id = %s"
    cur.execute(fil_mvmt, [v,])
    mvmt_list = list(cur.fetchall())

    # putting movement type within the list
    mvmt_li = []
    for mvmt in mvmt_list:
        mv = []
        for ind, i in enumerate(mvmt):
            if ind == 1:
                mvmt_t = "SELECT * FROM mvmt_types WHERE mt_id = %s"
                cur.execute(mvmt_t, [mvmt[1],])
                mt = cur.fetchone()[1]
                mv.append(mt)
            else:
                mv.append(i)
        mvmt_li.append(mv)

    sorted_list = sorted(mvmt_li, key=lambda t: datetime.strptime(t[12], '%Y-%m-%d %H:%M'))

    final_list = []
    for i in sorted_list:
        op_date = f'____________________DAY: {i[12][:10]}____________________'
        final_list.append(op_date)
        final_list.append(i[1:])

    res = []
    [res.append(x) for x in final_list if x not in res]

    mvmts = []
    for i in res:
        if 'DAY' in i:
            we = i[:25]
            ek = i[31:]
            week_title = we + ek
            mvmts.append(week_title)
        else:
            mvmts.append(i)

    cur.execute("SELECT * FROM assets")
    ass_list = cur.fetchall()
    
    return (mvmts, event_list, l, ass_list, mvmt_types, drivers)

def current_lto(ev):
    mydb, cur = check_db_connection()
    print(ev)
    cur.execute("DELETE FROM current_lto")
    print('removed old directory')

    sql_g = "SELECT * FROM events WHERE event_name = %s"
    cur.execute(sql_g, [ev,])
    e = cur.fetchone()
    print(f'got {e[0]} from database\n')

    ind = e[0]
    sql_q = "INSERT INTO current_lto (id, lto) VALUES (0, %s)"

    cur.execute(sql_q, [ind,])
    mydb.commit()
    mydb.close()
    print('\nsubmitted query\n')
    
    return (ind)

def create_event_timeline():
    mydb, cur = check_db_connection()
    cur.execute("SELECT event_name, start_d, end_d FROM events")
    event_list = cur.fetchall()
    
    df = pd.DataFrame(event_list, columns=['event', 'start date', 'end date']).rename(columns={'event':'Task', 'start date':'Start', 'end date':'Finish'})
    
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color='Task')
    fig.update_yaxes(autorange='reversed')

    title = 'All Events'

    now = datetime.now()

    today = now.strftime("%Y-%m-%d %H:%M")

    fig.update_layout(shapes=[dict(type='line', yref='paper', y0=0, y1=1, xref='x', x0=today, x1=today)], title=title,
                        plot_bgcolor='#3D4849', paper_bgcolor='#3D4849', legend_font_color='#FFFFFF',
                        legend_grouptitlefont_color='#FFFFFF', title_font_color='#FFFFFF', 
                        legend_title_font_color='#FFFFFF', font_color='#FFFFFF')

    graphSON = json. dumps (fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphSON

def create_movement_timeline():
    mydb, cur = check_db_connection()
    # grabbing lto index from current lto table
    cur.execute("SELECT * FROM current_lto")
    lto = cur.fetchone()[1]
    sql = "select call_sign, start_dt, end_dt from movements where event_id = %s"
    v = (lto, )
    cur.execute(sql, v)
    event_list = cur.fetchall()

    # grabbing current event name
    sq = "SELECT event_name FROM events where e_id = %s"
    n = (lto, )
    cur.execute(sq, n)
    title = f'Movements for {cur.fetchone()[0]}'

    df = pd.DataFrame(event_list, columns=['mvmt', 'start_dt', 'end_dt']).rename(columns={'mvmt':'Task', 'start_dt':'Start', 'end_dt':'Finish'})
    
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color='Task', labels='Task')
    fig.update_yaxes(autorange='reversed')

    now = datetime.now()

    today = now.strftime("%Y-%m-%d %H:%M")
    
    title = f'{title}'
    fig.update_layout(shapes=[dict(type='line', yref='paper', y0=0, y1=1, xref='x', x0=today, x1=today)], title=title,
                        plot_bgcolor='#3D4849', paper_bgcolor='#3D4849', legend_font_color='#FFFFFF',
                        legend_grouptitlefont_color='#FFFFFF', title_font_color='#FFFFFF', 
                        legend_title_font_color='#FFFFFF', font_color='#FFFFFF')

    graphSON = json. dumps (fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphSON

def create_mvmt_type(mvmt_name):
    mydb, cur = check_db_connection()
    sql = "INSERT INTO mvmt_types (mvmt_name) VALUES (%s)"
    cur.execute(sql, [mvmt_name,])
    mydb.commit()
    mydb.close()
    print('successfully submitted to database')

def create_driver(driver_name):
    mydb, cur = check_db_connection()
    sql = "INSERT INTO drivers (name) VALUES (%s)"
    cur.execute(sql, [driver_name,])
    mydb.commit()
    mydb.close()
    print('successfully submitted to database')