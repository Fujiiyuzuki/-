from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'secret_key'  # セッション用の秘密鍵

# 為替レート
exchange_rates = {
    'USD': 0.0072,  # 1円 = 0.0072ドル
    'EUR': 0.0066,  # 1円 = 0.0066ユーロ
    'KRW': 9.92     # 1円 = 9.92ウォン
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])  # 金額を数値に変換
            currency = request.form['currency']     # 通貨（USDなど）
            direction = request.form['direction']   # 換算方向

            rate = exchange_rates.get(currency)
            if rate is None:
                session['direction_str'] = '無効な通貨が選択されました。'
                return redirect(url_for('result'))

            if direction == 'to_foreign':
                result = round(amount * rate, 2)
                direction_str = f"{amount} 円 → {result} {currency}"
            else:
                result = round(amount / rate, 2)
                direction_str = f"{amount} {currency} → {result} 円"

            session['direction_str'] = direction_str
        except ValueError:
            session['direction_str'] = '金額は正しい数字で入力してください。'

        return redirect(url_for('result'))

    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True, port=8888)