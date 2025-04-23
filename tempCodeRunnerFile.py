#@app.route("/predict",methods=["GET","POST"])
# def hello_world():
#     if request.method=='POST':
#         Cement=float(request.form.get('Cement'))
#         BlastFurnaceSlag=float(request.form.get('BlastFurnaceSlag'))
#         FlyAsh=float(request.form.get('FlyAsh'))
#         Water=float(request.form.get('Water'))
#         Superplasticizer=float(request.form.get('Superplasticizer'))
#         Coarse=float(request.form.get('Coarse'))
#         FineAggregate=float(request.form.get('FineAggregate'))
#         Age=float(request.form.get('Age'))
#         result=model.predict([[ Cement, BlastFurnaceSlag,FlyAsh,Water,Superplasticizer, Coarse,FineAggregate,Age]])
#         if(result<0):
#            result=-result
#         return render_template('predict.html',results=result[0])

#     else:
#         return render_template('predict.html')