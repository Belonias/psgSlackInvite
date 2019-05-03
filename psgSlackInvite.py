from flask import Flask, render_template, url_for, flash, redirect
from forms import InviteForm
import requests
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]

@app.route("/home")
def landing_page():
	return render_template('home.html')

@app.route("/", methods=['GET', 'POST'])
@app.route("/invite", methods=['GET', 'POST'])
def invite():
	form = InviteForm()
	if form.validate_on_submit():
		invite_slack_result = invite_to_slack(form.email.data)
		print(invite_slack_result)
		if invite_slack_result["ok"]:
			flash('Invite send at {}'.format(form.email.data, 'success'))
		else:
			flash(invite_slack_result)
		return redirect(url_for('landing_page'))
	return render_template('invite.html', title='Invite', form=form)

def invite_to_slack(user_email):
	slack_request = 'https://slack.com/api/users.admin.invite?token='
	slack_token = os.environ["SLACK_API_TOKEN"]
	user_email = '&email=' + str(user_email)
	url = slack_request.strip() + slack_token.strip() + user_email.strip()
	r = requests.get(url)
	data = r.json()
	print(data["ok"])
	return data

if __name__ == '__main__':
	app.run()