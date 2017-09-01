import pysb
import os, time
from flask import Flask, url_for, render_template, jsonify
app = Flask(__name__)

##VARIABLES

#project_parent_id = "4f4e476fe4b07f02db47e19e"
#max_projects = "25"
#community_id = "57a8c92be4b0ebae89bafbee"
project_parent_id = "587fb88ee4b085de6c11f3bf"
max_projects = "25"
community_id = "5849798be4b06d80b7b0946b"
publications_id = "58ac9249e4b0ce4410e7d7e8"
home_site_intro_id = "57bdbcc1e4b03fd6b7df4463"
slider_images_id ='57bde986e4b03fd6b7df5f93'
news_id = '58ac67bfe4b0ce4410e7d6f2'
sb = pysb.SbSession()
# Get a private item.  Need to log in first.
assessment_filter = 'assessment'
username = raw_input("Username:  ")
sb.loginc(str(username))
# Need to wait a bit after the login or errors can occur
#time.sleep(0)



@app.route('/home/')	
def home():
	slider_urls = sb.get_item(slider_images_id)
	print (slider_urls["files"][1]["url"])
	home_site_news = sb.find_items('parentId=%s&sort=title&max=%s' %(news_id, max_projects))
	home_site_intro_all = sb.get_item(home_site_intro_id)
	home_site_intro = home_site_intro_all["summary"].replace("&nbsp;", "")
	assessments = sb.find_items('parentId=%s&sort=title&max=%s&filter=tags=%s' %(publications_id, max_projects,assessment_filter))
	#print(assessments['items'][0])
	for items in assessments['items']:
		print items["files"][1]["url"]
	extents = sb.find_items('parentId=%s&fields=title,spatial&max=%s' %(project_parent_id, max_projects))
	return render_template('index.html', home_site_intro=home_site_intro, extents=extents, slider_urls=slider_urls, home_site_news=home_site_news, assessments=assessments)

@app.route('/projects/')
def projects():
	items = sb.find_items('parentId=%s&sort=title&max=%s' %(project_parent_id, max_projects))
	return render_template('projects.html', items=items)
 
@app.route('/projects/<projectid>')
def project(projectid):
	item = sb.get_item(projectid)
	return render_template('project.html', item=item)

@app.route('/about')
def about():
	community_data = sb.get_item(community_id)
	return render_template('about.html', community_data=community_data)
	
@app.context_processor
def inject_title():
	community_title = sb.get_item(community_id)['title']
	return dict(community_title=community_title)
	
