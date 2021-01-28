from flask import Flask, render_template
from flask_socketio import  SocketIO, emit
from grzalka2 import Podgrzewacz
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
socketio = SocketIO(app)
socketio.run(app)

@socketio.on('calculate')
def generate_graph(json):
    print("Get calculate event")
    graf_nr = 0
    graf = '#graph1'
    grzalka = Podgrzewacz(float(json['U']), float(json['V']), float(json['temp0']),
        float(json['temp1']), float(json['flow'])*(10**(-3)), float(json['Kp']), float(json['Ti']),
        float(json['Td'])
    )
    grzalka.generate_data(float(json['tp']), float(json['tsim']))
    print(float(json['Kp']))
    n = [float(x*float(json['tp'])/60) for x in range(int(float(json['tsim'])/ float(json['tp']))) ]
    fig = make_subplots(rows=4, cols=1,
        subplot_titles=("Wykres temperatury od czasu", "Wykres napięcia sterującego od czasu", "Wykres napięcia na grzałce od czasu", "Wykres mocy grzałki od czasu")
    )
    fig.add_trace(go.Scatter(x=n, y=grzalka.temperatury, mode="lines", name="Temp."), row=1, col=1)
    fig.add_trace(go.Scatter(x=n, y=[grzalka.t_zad for i in range(len(grzalka.temperatury))], line=dict(dash='dash'), name="Temp. zadana"), row=1, col=1)
    fig.add_trace(go.Scatter(x=n, y=grzalka.u, mode="lines", name="u"), row=2, col=1)
    fig.add_trace(go.Scatter(x=n, y=grzalka.napiecia, mode="lines", name="U"), row=3, col=1)
    fig.add_trace(go.Scatter(x=n, y=grzalka.moc, mode="lines", name="P"), row=4, col=1)
    fig.update_xaxes(title_text="czas [min.]", row=1, col=1)
    fig.update_xaxes(title_text="czas [min.]", row=2, col=1)
    fig.update_xaxes(title_text="czas [min.]", row=3, col=1)
    fig.update_xaxes(title_text="czas [min.]", row=4, col=1)
    fig.update_yaxes(title_text="temp. wody [C]", row=1, col=1)
    fig.update_yaxes(title_text="napięcie sterujące [V]", row=2, col=1)
    fig.update_yaxes(title_text="napięcie grzałki [V]", row=3, col=1)
    fig.update_yaxes(title_text="moc grzałki [W]", row=4, col=1)
    fig.update_layout(template='plotly_dark')
    
    if json['graph'] == '#interface-1':
        fig.write_html("./static/graph1.html")
        graf_nr = 0
        graf = '#graph1'
    elif json['graph'] == '#interface-2':
        fig.write_html("./static/graph2.html")
        graf_nr = 1
        graf = '#graph2'
    print("finished graph")
    print("uchyb ustalony ", grzalka.uchyb_ustalony)
    print("przeregulowanie ", grzalka.przeregulowanie)
    print("dokladnosc regulacji ", grzalka.dokladnosc_regulacji)
    print("koszty regulacji ", grzalka.koszty_regulacji)
    data = {
        "graf": graf,
        "graf_nr": graf_nr,
        "uchyb": round(grzalka.uchyb_ustalony, 2),
        "przeregulowanie": round(grzalka.przeregulowanie, 2),
        "dokladnosc": round(grzalka.dokladnosc_regulacji, 0),
        "koszty": round(grzalka.koszty_regulacji, 0),
        "czas": round(grzalka.czas_regulacji, 2)
    }
    emit('calculated', data)

@app.route('/')
def index():
    data = []
    return render_template('index.html', data=data)