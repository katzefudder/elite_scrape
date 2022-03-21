import scrapy, re
from scrapy.http.request import Request

class EliteSpider(scrapy.Spider):
  name = "elite"

  results = {}
  content = ""

  teams = {
    'bn' : 'https://www.eliteprospects.com/team/438/ec-bad-nauheim?sort=jersey',
    'sw' : 'https://www.eliteprospects.com/team/662/selber-wolfe?sort=jersey',
    'fl' : 'https://www.eliteprospects.com/team/5065/lowen-frankfurt?sort=jersey',
    'bt' : 'https://www.eliteprospects.com/team/439/tolzer-lowen?sort=jersey',
    'by' : 'https://www.eliteprospects.com/team/746/bayreuth-tigers?sort=jersey',
    'dd' : 'https://www.eliteprospects.com/team/983/dresdner-eislowen?sort=jersey',
    'ka' : 'https://www.eliteprospects.com/team/8287/ec-kassel-huskies?sort=jersey',
    'fr' : 'https://www.eliteprospects.com/team/9328/ehc-freiburg?sort=jersey',
    'cr' : 'https://www.eliteprospects.com/team/659/eispiraten-crimmitschau?sort=jersey',
    'kb' : 'https://www.eliteprospects.com/team/677/esv-kaufbeuren?sort=jersey',
    'lh' : 'https://www.eliteprospects.com/team/642/ev-landshut?sort=jersey',
    'hn' : 'https://www.eliteprospects.com/team/444/heilbronner-falken?sort=jersey',
    'lf' : 'https://www.eliteprospects.com/team/448/lausitzer-fuchse?sort=jersey',
    'rt' : 'https://www.eliteprospects.com/team/747/ravensburg-towerstars?sort=jersey'
  }

  def parse(self, response):
    # invert the dict
    team_keys = dict(zip(self.teams.values(), self.teams.keys()))

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
    self.results[team_keys[response.url]] = content

  # write content to a file
  def writeFile(self, content):
    with open('del2.txt', 'w+') as f:
      f.write(content)

  # override start_request to use an own dict instead of start_urls
  def start_requests(self):
    for key, url in self.teams.items():
      yield Request(url, self.parse)

  def __del__(self):
    content = ""
    for key in sorted(self.results):
      content += self.results[key]
      
    self.writeFile(content)
