from flask import Flask, render_template,request,redirect, url_for, session
import pymysql
from os import path
mob=Flask(__name__)
mob.secret_key="mob7010"
mob.config["UPLOAD_FOLDER"]="static/upload_images/"
conn=pymysql.connect(host="localhost",user="root",password="12345678",db="mob")
@mob.route("/")
def home():

    user_id = ""
    u = ""
    e = ""
    a = ""
    mno = ""
    cur = conn.cursor()
    query = ''' SELECT * FROM products WHERE no_items>=1 AND pmode='visible'; '''
    cur.execute(query)
    r = cur.fetchall()
    if "email" not in session:
        u = ""
        e = ""
        user_id = ""
        a = ""
        mno = ""
        return render_template("home121.html", name=u, email=e, u_id=user_id, age=a, mobno=mno,rows=r)
    if session["email"]:
        user_id=session["u_id"]
        u=session["user_name"]
        e=session["email"]
        a=session["age"]
        mno=session["mob_no"]
        if e=="admin123@gmail.com":
            return redirect("/admin_dashboard")
    return render_template("home121.html", name=u, email=e, u_id=user_id, age=a, mobno=mno,rows=r)








@mob.route("/cart")
def cart():
    r=""
    if session:
        cur=conn.cursor()
        query=''' SELECT p.mob_model, p.price, p.image_path,
        t.p_items, t.total_amount, t.p_status,t.t_id
        FROM transactions t JOIN users u on t.tu_id=u.u_id JOIN products p on 
        t.tp_id=p.p_id WHERE t.tu_id={0} AND t.p_status='cart';
        '''.format(session["u_id"])
        cur.execute(query)
        r=cur.fetchall()
    if request.args.get("cart")=="cartpdt":
        uid=request.args.get("uid")
        pid=request.args.get("pid")
        noitems=request.args.get("noitems")
        price=request.args.get("price")
        total=float(price)*float(noitems)
        cur=conn.cursor()
        query=''' INSERT INTO transactions(tu_id,tp_id,p_items,total_amount) 
         VALUES('{0}','{1}','{2}','{3}');'''.format(uid,pid,noitems,total)
        cur.execute(query)
        conn.commit()
        cur.close()
        return redirect("/cart")
    if request.args.get("remove")=="removed":
        tid=request.args.get("tid")
        cur=conn.cursor()
        query=''' DELETE FROM transactions WHERE t_id='{0}'; '''.format(tid)
        cur.execute(query)
        conn.commit()
        cur.close()
        return redirect("/cart")
    return render_template("cart32.html",rows=r)






@mob.route("/history")
def history():
    r=""
    if session:
        cur=conn.cursor()
        query=''' SELECT p.mob_model, p.p_id,p.price, p.image_path,
        t.p_items, t.total_amount, t.p_status,t.p_date
        FROM transactions t JOIN users u on t.tu_id=u.u_id JOIN products p on 
        t.tp_id=p.p_id WHERE t.tu_id={0} AND t.p_status='purchased'; 
         '''.format(session["u_id"])
        cur.execute(query)
        r=cur.fetchall()
        cur.close()
    if request.args.get("check")=="checked":
        tid=request.args.get("tid")
        cur=conn.cursor()
        query=''' UPDATE transactions SET p_status='purchased' WHERE t_id='{0}'; 
        '''.format(tid)
        cur.execute(query)
        conn.commit()
        cur.close()
    return render_template("purchase.html",rows=r)






@mob.route("/login")
def login():
    e=""
    if request.args.get("log")=="logged":
        email=request.args.get("mail")
        pwd=request.args.get("pass")
        cur=conn.cursor()
        query=''' SELECT * FROM users WHERE email='{0}' AND pass='{1}'; '''.format(email,pwd)
        cur.execute(query)
        row=cur.fetchone()
        if row:
            session["u_id"] = row[0]
            session["user_name"] = row[1]
            session["age"] = row[2]
            session["mob_no"] = row[3]
            session["email"] = row[4]
            session["password"] = row[5]
            return redirect("/")
        else:
            e="Invalid Email or Password"
            return render_template("loginform12.html",err=e)
    return render_template("loginform12.html",err=e)






@mob.route("/register")
def register():
    s=""
    e=""
    if request.args.get("reg")=="registered":
        name=request.args.get("name")
        age=request.args.get("age")
        mobno=request.args.get("mobno")
        email=request.args.get("mail")
        pwd=request.args.get("pass")
        cur=conn.cursor()
        query=''' SELECT email FROM users WHERE email='{0}'; '''.format(email)
        cur.execute(query)
        checkEmail=cur.fetchone()
        if checkEmail:
            e="Email Already exists!.."
        else:
            query=''' INSERT INTO users(user_name, age, mob_no, email, pass )
             VALUES ('{0}','{1}','{2}','{3}','{4}');'''.format(name,age,mobno,email,pwd)
            cur.execute(query)
            conn.commit()
            s="Succesfully Registered!.."
    return render_template("regform12.html",success=s,err_email=e)





@mob.route("/logout")
def logout():
    session.clear()
    return redirect("/")





@mob.route("/admin_dashboard")
def admin():
    cur = conn.cursor()
    query = '''SELECT count(user_name) FROM users; '''
    cur.execute(query)
    n = cur.fetchone()
    query = "SELECT count(mob_name) FROM products WHERE pmode='visible';"
    cur.execute(query)
    n2 = cur.fetchone()
    query=''' SELECT count(t_id) FROM transactions WHERE p_status='purchased'; '''
    cur.execute(query)
    n3=cur.fetchone()
    query=''' SELECT * FROM products WHERE pmode="visible"; '''
    cur.execute(query)
    r=cur.fetchall()
    cur.close()
    return render_template("admin583.html",rows=r, no=n[0], no_m=n2[0],no_s=n3[0])





@mob.route("/admin_dashboard/add_mobiles",methods=["GET","POST"])
def add_mobiles():
    filepath = ""
    s=""
    if request.method=="POST":
        name=request.form["name"]
        model=request.form["model"]
        no=request.form["items"]
        price=request.form["price"]
        image=request.files["mobimage"]
        if image.filename!="":
            filepath=path.join(mob.config["UPLOAD_FOLDER"],image.filename)
            image.save(filepath)
            cur=conn.cursor()
            query=''' INSERT INTO products(mob_name,mob_model,no_items,price,image_path)
             VALUES('{0}','{1}','{2}','{3}','{4}');'''.format(name,model,no,price,filepath)
            cur.execute(query)
            conn.commit()
            s="Successfully Added!..."
    return render_template("addmob45.html",path=filepath,success=s)





@mob.route("/admin_dashboard/edit_mobiles",methods=["GET","POST"])
def edit_mobiles():
    jid = ""
    name = ""
    model = ""
    items =""
    price = ""
    imagepath = ""
    if request.method=="GET" and request.args.get("edit")=="edited":
        pid=request.args.get("id")
        cur=conn.cursor()
        query=''' SELECT * FROM products WHERE p_id='{0}';
        '''.format(pid)
        cur.execute(query)
        r=cur.fetchone()
        cur.close()
        jid=r[0]
        name=r[1]
        model=r[2]
        items=r[3]
        price=r[4]
        imagepath=r[5]
        return render_template("updatemob635.html",a_id=jid ,a_name=name, a_model=model, a_items=items, a_price=price,
                               a_image=imagepath)
    if request.method=="POST":
        cid=request.form["cid"]
        cname=request.form["cname"]
        cmodel=request.form["cmodel"]
        citems=request.form["citems"]
        cprice=request.form["cprice"]
        cimage=request.files["cmobimage"]
        if cimage.filename!="":
            cimagepath=path.join(mob.config["UPLOAD_FOLDER"],cimage.filename)
            cimage.save(cimagepath)
            cur=conn.cursor()
            query=''' UPDATE products SET mob_name='{0}',mob_model='{1}',no_items='{2}',
                price='{3}',image_path='{4}' WHERE p_id="{5}" ;
                 '''.format(cname,cmodel,citems,cprice,cimagepath,cid)
            cur.execute(query)
            conn.commit()
            return redirect("/admin_dashboard")
    return render_template("updatemob635.html",a_id=jid,a_name=name,a_model=model,a_items=items,a_price=price,a_image=imagepath)





@mob.route("/admin_dashboard/delete_mobiles")
def delete_mobiles():
    if request.args.get("rem")=="removed":
        pid=request.args.get("id")
        cur=conn.cursor()
        query=''' UPDATE products SET pmode='hide' WHERE p_id="{0}"; '''.format(pid)
        cur.execute(query)
        conn.commit()
        cur.close()
    return redirect("/admin_dashboard")





if __name__=="__main__":
    mob.run(debug=True)