from flask import Flask, render_template, url_for, flash, redirect
from forms import InviteForm
import requests
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]

@app.route("/welcome")
def welcome():
	return render_template('welcome.html')


@app.route("/already_in_team")
def already_in_team_error():
	'''User is already member in the team'''
	return render_template('already_in_team.html')


@app.route("/already_invited")
def already_invited_error():
	'''User has already invited'''
	return render_template('already_invited.html')


@app.route("/invalid_email")
def invalid_email_error():
	'''User has already invited'''
	return render_template('invalid_email.html')


@app.route("/", methods=['GET', 'POST'])
@app.route("/invite", methods=['GET', 'POST'])
def invite():
	form = InviteForm()
	if form.validate_on_submit():
		invite_slack_result = invite_to_slack(form.email.data)
		print(invite_slack_result)
		if invite_slack_result["ok"]:
			flash('Invite send at {}'.format(form.email.data, 'success'))
			return(redirect(url_for('welcome')))
		elif invite_slack_result["ok"] is False and invite_slack_result["error"] == "already_in_team":
			flash('There is already a user in the team with the email {}'.format(form.email.data, 'error'))
			return(redirect(url_for('already_in_team_error')))
		elif invite_slack_result["ok"] is False and invite_slack_result["error"] == "already_invited":
			flash('The invitation has already been sent at {}'.format(form.email.data, 'error'))
			return(redirect(url_for('already_invited_error')))
		elif invite_slack_result["ok"] is False and invite_slack_result["error"] == "already_invited":
			flash('The email {} is invalid'.format(form.email.data, 'error'))
			flash('Note that slack does not recognise some email addresses'.format())
			return(redirect(url_for('invalid_email_error')))

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
