from flask import Flask, render_template, request, redirect
from datetime import datetime
import os

app = Flask(__name__)

# Дауыс беру тарихы (Сервер қосулы тұрғанда сақталады)
vote_history = []

@app.route('/')
def index():
    return render_template('nono.html')

@app.route('/vote', methods=['POST'])
def vote():
    voter_name = request.form.get('voter')
    choice = request.form.get('candidate')
    
    # Қазіргі уақыт
    current_time = datetime.now().strftime("%H:%M:%S")
    display_choice = "1-тұлға" if choice == "A" else "2-тұлға"
    
    vote_history.insert(0, {
        'name': voter_name, 
        'choice': display_choice, 
        'time': current_time
    })
    
    return redirect('/results')

@app.route('/results')
def results():
    count_1 = sum(1 for v in vote_history if v['choice'] == "1-тұлға")
    count_2 = sum(1 for v in vote_history if v['choice'] == "2-тұлға")
    
    history_html = "".join([
        f"<div style='background: rgba(255,255,255,0.05); margin: 10px 0; padding: 15px; border-radius: 10px; border-left: 4px solid #00c6ff; display: flex; justify-content: space-between; align-items: center;'>"
        f"<span><b>{v['name']}</b> — {v['choice']}</span>"
        f"<span style='font-size: 12px; color: #888;'>🕒 {v['time']}</span></div>" 
        for v in vote_history
    ])

    return f"""
    <div style="background: #0a0a0a; color: white; min-height: 100vh; padding: 50px; font-family: 'Segoe UI', sans-serif;">
        <div style="max-width: 600px; margin: 0 auto;">
            <h1 style="text-align: center; font-weight: 300; letter-spacing: 2px;">📊 ДАУЫС БЕРУ ЖУРНАЛЫ</h1>
            <div style="display: flex; justify-content: space-around; margin-bottom: 40px; background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px;">
                <div style="text-align: center;">
                    <div style="font-size: 12px; color: #aaa;">1-ТҰЛҒА</div>
                    <div style="font-size: 32px; color: #00c6ff; font-weight: bold;">{count_1}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 12px; color: #aaa;">2-ТҰЛҒА</div>
                    <div style="font-size: 32px; color: #0072ff; font-weight: bold;">{count_2}</div>
                </div>
            </div>
            <h3>Соңғы әрекеттер:</h3>
            <div>{history_html if vote_history else "<p>Тізім бос...</p>"}</div>
            <br><a href='/' style="color: #00c6ff; text-decoration: none;">← Артқа қайту</a>
        </div>
    </div>
    """

if __name__ == '__main__':
    # Хостинг үшін маңызды бөлік:
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)