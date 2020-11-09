from flask import Flask,send_file

app=Flask(__name__)

@app.route('/index.html')
def index():
    #首页
    return send_file('templates/index.html')
@app.route('/header.html')
def header():
    #首页
    return send_file('templates/header.html')

@app.route('/footer.html')
def footer():
    #首页
    return send_file('templates/footer.html')

@app.route('/login.html')
def login():
    # 登录
    return send_file('templates/login.html')
@app.route('/register_sms.html')
def register():
    #注册
    return send_file('templates/register_sms.html')
@app.route('/callback')
def callback():
    #授权登录
    return send_file('templates/callback.html')

@app.route('/cart.html')
def cart():
    #购物车
    return send_file('templates/cart.html')

@app.route('/addressAdmin.html')
def addressAdmin():
    #购物车
    return send_file('templates/addressAdmin.html')

@app.route('/myOrder.html')
def myOrder():
    #订单信息
    return send_file('templates/myOrder.html')

@app.route('/orderConfirm.html')
def orderConfirm():
    #订单信息
    return send_file('templates/orderConfirm.html')


@app.route('/<username>/gopay.html')
def gopay(username):
    #订单信息
    return send_file('templates/gopay.html')

@app.route('/payment.html')
def payment():
    #订单信息http://127.0.0.1:5000/payment.html?address_id=1&settlement_type=0
    return send_file('templates/payment.html')

@app.route('/pay_success.html')
def pay_success():
    #订单信息
    return send_file('templates/pay_success.html')

@app.route('/findPass(备注).html')
def findPass():
    #找回密码
    return send_file('templates/findPass(备注).html')

@app.route('/product_list.html')
def product_list():
    #个人博客列表
    return send_file('templates/product_list.html')

@app.route('/product_details.html')
def product_detail():
    #博客内容详情
    return send_file('templates/product_details.html')
@app.route('/personal_password.html')
def personal_password():
    # 登录
    return send_file('templates/personal_password.html')




@app.route('/search')
def search():
    #测试
    return send_file('templates/search.html')

if __name__ == '__main__':
    app.run(debug=True)