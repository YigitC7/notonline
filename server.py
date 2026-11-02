from flask import Flask, render_template, request, url_for, session, redirect, jsonify
import database
import ast

class Server:
    def __init__(self):
        self.flaskRoot = Flask(__name__)
        self.flaskRoot.secret_key = "UIGHIUGTYfdgw7852323hrfYFyt67"

        self.Pages()
        self.LocalApi()
        self.ErrorPages()

    def Pages(self):

        @self.flaskRoot.route("/",methods=["GET"])
        def home():
            if not session.get("username"):
                return render_template("home.html")

            booknames = database.books.books_get(session.get("username"))
            return render_template("userpanel.html", books=booknames, username=session.get("username"))

        @self.flaskRoot.route("/kayit",methods=["POST","GET"])
        def kayit():
            if request.form.get("username") and request.form.get("password") and request.form.get("password2"):
                
                statu = database.users.add(
                    username= request.form.get("username"),
                    password= request.form.get("password"),
                    password2= request.form.get("password2")
                )

                if statu != "ok":
                    return render_template("kayit.html", message=statu)
                else:
                    session["username"] = request.form.get("username")
                    return redirect(url_for("home"))
                
            return render_template("kayit.html")

        @self.flaskRoot.route("/giris",methods=["POST","GET"])
        def giris():
            if request.form.get("username") and request.form.get("password"):
                statu = database.users.login(
                    username= request.form.get("username"),
                    password= request.form.get("password")
                )

                if statu != "ok":
                    return render_template("giris.html", message=statu)
                else:
                    session["username"] = request.form.get("username")
                    return redirect(url_for("home"))

            return render_template("giris.html")

        @self.flaskRoot.route("/yeni-defter",methods=["POST"])
        def yeni_defter():
            if not session.get("username"):
                return render_template("error.html")
            
            if request.form.get("bookname"):
                if not request.form.get("public"):
                    public = 0
                else:
                    public = 1

                statu = database.books.new(
                    username= session.get("username"),
                    bookname= request.form.get("bookname"),
                    public= public
                )

                if statu != "ok":
                    return render_template("yenidefter.html", message=statu)
                else:
                    return redirect(url_for("defter",username=session.get("username"),bookname=request.form.get("bookname")))
            
            return render_template("yenidefter.html")

        @self.flaskRoot.route("/defter/<username>/<bookname>", methods=["GET"])
        def defter(username, bookname):
            try:
                NoteDatas = database.books.bookDatas(username,bookname)
                if NoteDatas[3] == None:
                    YetkiliKisiler = []
                else:
                    YetkiliKisiler = ast.literal_eval(NoteDatas[3])
            except ValueError:
                pass
            except TypeError:
                return render_template("404.html")

            
            if session.get("username"):
                
                if NoteDatas[0] == session.get("username")  or (session.get("username") in YetkiliKisiler):
                    session["write"] = bookname
                    return render_template("NoteW.html", NoteDatas=NoteDatas)
            
            if NoteDatas[4] == 1:
                return render_template("NoteR.html", NoteDatas=NoteDatas)

            return render_template("404.html")

        @self.flaskRoot.route("/defter/i/<username>/<bookname>",methods=["GET"])
        def defterI(username,bookname):
            try:
                NoteDatas = database.books.bookDatas(username,bookname)
                NoteDatas = list(NoteDatas)
            except TypeError:
                return render_template("404.html")
            
            if session.get("username"):

                if NoteDatas[3]:
                    NoteDatas[3] = ast.literal_eval(NoteDatas[3])

                if NoteDatas[0] == session.get("username"):
                    session["Admin"] = bookname
                    
                    return render_template("noteInfoAdmin.html", NoteDatas= NoteDatas)

            if NoteDatas[4] == 1:
                return render_template("noteInfo.html", NoteDatas= NoteDatas)

            return render_template("404.html")


    def LocalApi(self):

        @self.flaskRoot.route("/local-api/kaydet", methods=["POST"])
        def kaydet():
            PostDatas = request.get_json() 
            if PostDatas.get("notes") and PostDatas.get("creater_username") and PostDatas.get("bookname") and session.get("username"):

                if session.get("write") == PostDatas.get("bookname"):
                    
                    for i in range(1,len(PostDatas["notes"].keys())+1):
                        if len(PostDatas["notes"][f"{i}"]) > 80000:
                            return jsonify({"Error" : "High Character Limit"})
                    
                    database.books.bookSave(
                        username= PostDatas["creater_username"],
                        bookname= PostDatas["bookname"],
                        notes=  str(PostDatas["notes"])
                    )
                    return jsonify({"statu":"ok"})
                else:
                    return jsonify({"Error" : "No Authority"})
            else:
                return jsonify({"Error" : "No Datas"})

        @self.flaskRoot.route("/local-api/defter-ayar/gorunurluk", methods=["POST"])
        def ayar_gorunurluk():
            if session.get("username") and request.form.get("public") and request.form.get("creater_username") and request.form.get("bookname"):

                if session.get("Admin") == request.form.get("bookname"):
                    session.pop("Admin")
                    
                    statu = database.books.bookpublicUpdate(
                        username= request.form.get("creater_username"),
                        bookname= request.form.get("bookname"),
                        value= int(request.form.get("public"))
                    )

                    if statu == "ok":
                        return redirect(url_for(
                            "defterI",
                            username=request.form.get("creater_username"),
                            bookname= request.form.get("bookname"))
                            )
                    else:
                        return render_template("error.html")
                    
                else:
                    return render_template("error.html")

        @self.flaskRoot.route("/local-api/defter-ayar/yetkili-kullanici/ekle", methods=["POST"])
        def ayar_yetkili_kullanici_ekle():
            if session.get("username") and request.form.get("username") and request.form.get("creater_username") and request.form.get("bookname") and request.form.get("kisiler"):
                
                if session.get("Admin") == request.form.get("bookname"):
                    session.pop("Admin")

                    if request.form.get("kisiler") != "None":
                        kisiler = ast.literal_eval(request.form.get("kisiler"))

                        if session.get("username") == request.form.get("username"):
                            print(1)
                            return redirect(url_for(
                                "defterI",
                                username=request.form.get("creater_username"),
                                bookname= request.form.get("bookname")))


                        if not request.form.get("username") in kisiler:
                            kisiler.append(request.form.get("username"))
                        else:
                            return redirect(url_for(
                                "defterI",
                                username=request.form.get("creater_username"),
                                bookname= request.form.get("bookname")))

                    else:
                        kisiler = [request.form.get("username")]

                    statu = database.books.yetkiliguncelle(
                        username= request.form.get("creater_username"),
                        bookname= request.form.get("bookname"),
                        yetkili_adi= str(kisiler)
                    )

                    if statu == "ok":
                        return redirect(url_for(
                            "defterI",
                            username=request.form.get("creater_username"),
                            bookname= request.form.get("bookname"))
                            )
                    else:
                        return render_template("error.html")
                else:
                    return render_template("error.html")
            else:
                return render_template("error.html")

        @self.flaskRoot.route("/local-api/defter-ayar/yetkili-kullanici/kaldir", methods=["POST"])
        def ayar_yetkili_kullanici_kaldir():
            if session.get("username") and request.form.get("username") and request.form.get("creater_username") and request.form.get("bookname") and request.form.get("kisiler"):
                if session.get("Admin") == request.form.get("bookname"):
                    session.pop("Admin")
                    kisiler = ast.literal_eval(request.form.get("kisiler"))

                    try:
                        kisiler.remove(request.form.get("username"))
                    except ValueError:
                        return redirect(url_for(
                            "defterI",
                            username=request.form.get("creater_username"),
                            bookname= request.form.get("bookname"))
                            )

                    statu = database.books.yetkiliguncelle(
                        username= request.form.get("creater_username"),
                        bookname= request.form.get("bookname"),
                        yetkili_adi= str(kisiler)
                    )

                    if statu == "ok":
                        return redirect(url_for(
                            "defterI",
                            username=request.form.get("creater_username"),
                            bookname= request.form.get("bookname"))
                            )
                    else:
                        return render_template("error.html")
                else:
                    return render_template("error.html")
            else:
                return render_template("error.html")

        @self.flaskRoot.route("/local-api/defter/kaldir", methods=["POST"])
        def defter_kaldir():
            if request.form.get("book") and session.get("username"):
                statu = database.books.book_sil(
                    bookname= request.form.get("book"),
                    username= session.get("username")
                )

                if statu == "ok":
                    return redirect(url_for("home"))
                else:
                    return render_template("error.html")
            else:
                return render_template("error.html")

        @self.flaskRoot.route("/local-api/cikis-yap",methods=["POST"])
        def cikis_yap():
            session.clear()
            return redirect(url_for("home"))


    def ErrorPages(self):
        @self.flaskRoot.errorhandler(404)
        def sayfa_bulunamadi(error):
            return render_template("404.html"),404

        @self.flaskRoot.errorhandler(405)
        def beklenmeyen_hata(error):
            return render_template("error.html"),405


        


database.TableCreate()
Server().flaskRoot.run(debug=True, host="0.0.0.0")