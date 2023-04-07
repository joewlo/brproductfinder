from flask import Flask, redirect, render_template, request, url_for
import os

import openai

app = Flask(__name__)

openai.api_key = os.environ['OPENAI_API_KEY']


def generate_prompt(broadridgeproductname):
  return """Please explain what this Broadridge Financial Solutions product name stands for. Make the answer up to 150 words. Do not hallucinate.

Some examples:
Broadridge Financial Solutions Product Name: Gloss
Explanation: Global Settlement System. A multi-currency, multi-instrument, multi-language clearance settlement and accounting engine that allows for trading, financing and profit and loss calculations for global markets (excluding North America). Part of Global Technology & Operations (GTO) of Broadridge.
Broadridge Financial Solutions Product Name: Investor Mailbox
Explanation: A portal that provides access to company annual reports, prospectuses, issuers and fund communications highlighting stock and investment performance, trade confirmations, annual meetings notices as well as securities class action and corporate actions activity.

Broadridge Financial Solutions Product Name: {}
Explanation: """.format(broadridgeproductname.capitalize())


@app.route("/", methods=("GET", "POST"))
def index():
  if request.method == "POST":
    broadridgeproductname = request.form["broadridgeproductname"]
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=generate_prompt(broadridgeproductname),
      temperature=0,
      max_tokens=150)
    return redirect(url_for("index", result=response.choices[0].text))

  result = request.args.get("result")
  return render_template("index.html", result=result)


app.run(host='0.0.0.0', port=81)
