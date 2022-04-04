import scrapy, re
from scrapy.http.request import Request

class EliteSpider(scrapy.Spider):
  name = "elite"

  content = ""

  teams = {
    'str' : 'https://www.del-2.org/teamstripes/'
  }

  def parse(self, response):
    # invert the dict
    team_keys = dict(zip(self.teams.values(), self.teams.keys()))

    page = response.url.split('/')[-1]
    filename = '%s.txt' % page

    # get the team's name
    team = str(response.css('#wrapper_border #subcontent h1::text').get()).strip()

    # set a title
    content = "- " + str(team) + " -\n\n"

    for players in response.xpath('//*[@id="tabelle"]//tbody/tr'):
      current_team_key = team_keys[response.url]
      
      number = players.xpath('td[1]//text()').get().strip()
      prename = players.xpath('td[4]//text()').get().strip()
      name = players.xpath('td[3]//b//text()').get().strip()
      content += "%s%s\t-%s- %s %s (%s)\n" % (current_team_key, number, number, prename, name, team)

    self.content += content

  # write content to a file
  def writeFile(self, content):
    with open('team_stripes.txt', 'w+') as f:
      f.write(content)

  # override start_request to use an own dict instead of start_urls
  def start_requests(self):
    for key, url in self.teams.items():
      yield Request(url, self.parse)

  def __del__(self):
    self.writeFile(self.content)
