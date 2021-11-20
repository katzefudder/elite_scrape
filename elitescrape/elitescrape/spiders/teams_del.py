import scrapy, re
from scrapy.http.request import Request

class EliteSpider(scrapy.Spider):
  name = "elite"

  content = ""

  teams = {
    'am' : 'https://www.eliteprospects.com/team/119/adler-mannheim?sort=jersey',
    'rb' : 'https://www.eliteprospects.com/team/981/ehc-munchen?sort=jersey',
    'wb' : 'https://www.eliteprospects.com/team/975/grizzlys-wolfsburg?sort=jersey',
    'nb' : 'https://www.eliteprospects.com/team/130/nurnberg-ice-tigers?sort=jersey',
    'ap' : 'https://www.eliteprospects.com/team/120/augsburger-panther?sort=jersey',
    'eb' : 'https://www.eliteprospects.com/team/122/eisbaren-berlin?sort=jersey',
    'ir' : 'https://www.eliteprospects.com/team/475/iserlohn-roosters?sort=jersey',
    'sw' : 'https://www.eliteprospects.com/team/132/schwenninger-wild-wings?sort=jersey',
    'bs' : 'https://www.eliteprospects.com/team/440/bietigheim-steelers?sort=jersey',
    'ei' : 'https://www.eliteprospects.com/team/445/erc-ingolstadt?sort=jersey',
    'kp' : 'https://www.eliteprospects.com/team/127/krefeld-pinguine?sort=jersey',
    'st' : 'https://www.eliteprospects.com/team/447/straubing-tigers?sort=jersey',
    'de' : 'https://www.eliteprospects.com/team/133/dusseldorfer-eg?sort=jersey',
    'ft' : 'https://www.eliteprospects.com/team/441/fischtown-pinguins?sort=jersey',
    'kh' : 'https://www.eliteprospects.com/team/128/kolner-haie?sort=jersey'
  }

  def parse(self, response):
    # invert the dict
    team_keys = dict(zip(self.teams.values(), self.teams.keys()))

    page = response.url.split('/')[-1]
    filename = '%s.txt' % page

    # get the team's name
    team = str(response.css('#name-and-logo h1.semi-logo::text').get()).strip()

    # select coach
    headCoach = response.xpath("//text()[contains(., 'Head Coach')]/following::a[1]/text()").extract()
    # select assistant coach
    assistantCoach = response.xpath("//text()[contains(., 'Asst. Coach')]/following::a[1]/text()").extract()

    # set a title
    content = "- " + str(team) + " -\n\n"

    for players in response.css('table.roster tbody tr'):
      current_team_key = team_keys[response.url]
      number = str(players.css('td.jersey::text').get()).strip()

      number = number.replace('#', '')
      name = str(players.css('td a::text').get()).strip()
      # remove any hints on the player's name
      name = str(re.sub('\(.*\)', '', name)).strip()
      if number != 'None' and name != 'None':
        content += "%s%s\t-%s- %s (%s)\n" % (current_team_key, number, number, name, team)


    if headCoach:
      content += "%s100\t%s (Trainer %s)\n" % (current_team_key, headCoach[0].strip(), team)
    if assistantCoach:
      content += "%s101\t%s (Co-Trainer %s)\n" % (current_team_key, assistantCoach[0].strip(), team)

    content += "\n\n"
    self.content += content

  # write content to a file
  def writeFile(self, content):
    with open('del.txt', 'w+') as f:
      f.write(content)

  # override start_request to use an own dict instead of start_urls
  def start_requests(self):
    for key, url in self.teams.items():
      yield Request(url, self.parse)

  def __del__(self):
    self.writeFile(self.content)
