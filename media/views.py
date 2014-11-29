from sys import maxint
from django.core import serializers
from django.http import HttpResponse
from django.template import RequestContext, loader
from bs4 import BeautifulSoup
from urllib2 import urlopen
from time import sleep
from random import randint

from media.models import Video, Audio, Cartoon

# the base media urls from which to grab the data
BASE_VIDEO_URL   = "http://bbs.my2500.com/vod/"
BASE_AUDIO_URL   = "http://bbs.my2500.com/lymp3/"
BASE_CARTOON_URL = "http://g.e-hentai.org/?f_doujinshi=1&f_manga=1&f_artistcg=1&f_gamecg=1&f_western=1&f_non-h=1&f_imageset=1&f_cosplay=1&f_asianporn=1&f_misc=1&f_search=%E6%B1%89%E5%8C%96&f_apply=Apply+Filter"

def video_index(request):
	template = loader.get_template('video/index.html')
	context  = RequestContext(request, {'video_list': Video.objects.all()})
	return HttpResponse(template.render(context))

def audio_index(request):
	template = loader.get_template('audio/index.html')
	context  = RequestContext(request, {'audio_list': Audio.objects.all()})
	return HttpResponse(template.render(context))

def cartoon_index(request):
	template = loader.get_template('cartoon/index.html')
	context  = RequestContext(request, {'cartoon_list': Cartoon.objects.all()})
	return HttpResponse(template.render(context))

def video_detail(request, video_id):
	return HttpResponse("You're looking at video %s." % video_id)

def audio_detail(request, audio_id):
	return HttpResponse("You're looking at audio %s." % audio_id)

def cartoon_detail(request, cartoon_id):	
	return HttpResponse("You're looking at cartoon: %s." % cartoon_id)

def video_search(request):
	# declare empty results list
	results = []

	# query on name or range
	if 'name' in request.GET:
		name = request.GET['name']
		results = Video.objects.filter(name__contains=name)
	elif 'start' in request.GET and 'count' in request.GET:
		start = max(int(request.GET['start']), 0)
		stop  = max(int(request.GET['count']), 0) + start		
		results = Video.objects.all()[start:stop]

	# send back the response in html or json format
	if 'html' in request.GET:
		template = loader.get_template('video/index.html')
		context  = RequestContext(request, {'video_list': results})
		return HttpResponse(template.render(context))
	else:
		jsonData = serializers.serialize("json", results)
		return HttpResponse(jsonData)

def audio_search(request):
	# declare empty results list
	results = []

	# query on name or range
	if 'name' in request.GET:
		name = request.GET['name']
		results = Audio.objects.filter(name__contains=name)
	elif 'start' in request.GET and 'count' in request.GET:
		start = max(int(request.GET['start']), 0)
		stop  = max(int(request.GET['count']), 0) + start		
		results = Audio.objects.all()[start:stop]

	# send back the response in html or json format
	if 'html' in request.GET:
		template = loader.get_template('audio/index.html')
		context  = RequestContext(request, {'audio_list': results})
		return HttpResponse(template.render(context))
	else:
		jsonData = serializers.serialize("json", results)
		return HttpResponse(jsonData)

def cartoon_search(request):
	# declare empty results list
	results = []

	# query on name or range
	if 'name' in request.GET:
		name = request.GET['name']
		results = Cartoon.objects.filter(name__contains=name)
	elif 'start' in request.GET and 'count' in request.GET:
		start = max(int(request.GET['start']), 0)
		stop  = max(int(request.GET['count']), 0) + start		
		results = Cartoon.objects.all()[start:stop]

	# send back the response in html or json format
	if 'html' in request.GET:
		template = loader.get_template('cartoon/index.html')
		context  = RequestContext(request, {'cartoon_list': results})
		return HttpResponse(template.render(context))
	else:
		jsonData = serializers.serialize("json", results)
		return HttpResponse(jsonData)

def update_media(request):
	# delete all old items
	Video.objects.all().delete()
	Audio.objects.all().delete()
	Cartoon.objects.all().delete()	

	# parse and update media resources
	parse_and_update_video()
	parse_and_update_audio()
	parse_and_update_cartoon()

	return HttpResponse("OK")

def parse_and_update_video():	
	# open and extract the html pages	
	video_page_urls = [str(x*200) + '~' + str((x+1)*200) + '.htm' for x in range(10)]	
	video_urls = [BASE_VIDEO_URL + video_page_url for video_page_url in video_page_urls]
	data   = [urlopen(video_url) for video_url in video_urls]
	soups  = [BeautifulSoup(d, "html.parser", from_encoding="GBK") for d in data]
	entire = [soup.findAll('tr') for soup in soups]

	for rows in entire:
		for row in rows[1:]:
			for col in row.findAll('td'):
				try:
					name   = ''
					image  = ''
					url    = ''
					format = '.mp4'

					if len(col.text) > 0:
						name = col.text[:col.text.find('http:')]

					if col.img:
						image = BASE_VIDEO_URL + col.img['src']

					if col.a:
						url = col.a['href']

					if url[url.rfind('/'):].rfind('.') != -1:
						format = url[url.rfind('.'):]

					if name != '' and url != '':
						video = Video.objects.create_video(name=name, image=image, url=url, format=format)
						video.save()
				except:
					pass

def parse_and_update_audio():		
	# open and parse the html 	
	data = urlopen(BASE_AUDIO_URL)
	soup = BeautifulSoup(data, "html.parser", fromEncoding="GBK")

	i = 0
	for row in soup.findAll('tr'):
		i %= 4
		try:
			if i == 0:
				audio = Audio.objects.create_audio(name='', url='', intro='', duration='')
				if row.text.strip() != '':
					audio.name = row.td.text
					i += 1
			elif i == 1:
				audio.name = row.td.text
			elif i == 2:
				audio.intro    = row.findAll('br')[0].previousSibling.strip()
				audio.duration = row.findAll('br')[0].nextSibling.strip()
			else:
				src   = row.embed['src']
				start = src.find('http:')
				stop  = src.find('.mp3&') + 4
				audio.url = src[start:stop]
				audio.save()
		except:
			pass			
		i += 1				

def parse_and_update_cartoon():
	pages = BeautifulSoup(urlopen(BASE_CARTOON_URL), "html.parser")
	ptt   = pages.findAll('table', {'class':'ptt'})[0]
	turl  = ptt.findAll('a')[1]['href']  # template url
	last  = ptt.findAll('a')[-2]['href'] # last url
	count = int(last[last.find('=')+1:last.find('&')]) + 1

	# construct all urls
	head  = turl[:turl.find('=') + 1]
	tail  = turl[turl.find('=') + 2:]
	purls = [head + str(i) + tail for i in range(count)]

	for purl in purls:
		try:
			print(purl)
			page  = BeautifulSoup(urlopen(purl), "html.parser")
			table = page.findAll('table', {'class':'itg'})[0]
			rows  = table.findAll('tr')[1:]
			# for each cartoon
			for row in rows:	
				try:
					it5 = row.findAll('div', {'class':'it5'})
					if len(it5) == 0:	
						continue

					# get the name of this cartoon	
					name = it5[0].a.text	
					print(name)		

					# navigate to cartoon page and get all picture items
					soup = BeautifulSoup(urlopen(it5[0].a['href']), "html.parser")
					gdtm = soup.findAll('div', {'class':'gdtm'})

					# # get the cover image
					image = soup.findAll('div', {'id':'gleft'})[0].img['src']

					# get url of each picture of this cartoon
					urls = []
					for m in gdtm:
						pic_soup = BeautifulSoup(urlopen(m.a['href']), "html.parser")
						sleep(5 + randint(-1, 1) * randint(1, 3))
						urls.append(max([img['src'] for img in pic_soup.findAll('img')], key=len))
						print(max([img['src'] for img in pic_soup.findAll('img')], key=len))
					
					# create a new Cartoon object and save it to database
					cartoon = Cartoon.objects.create_cartoon(name=name, image=image, urls=urls)
					cartoon.save()
				except:
					print('Something wrong')
		except:
			print("can't open %s" % purl)





	
