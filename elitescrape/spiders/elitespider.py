import scrapy, re
import yaml
from scrapy.http.request import Request

class EliteSpider(scrapy.Spider):
  name = ""
  custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
  }
  league_key = ''
  teams_file = ""
  team_keys = ""

  teams = {}
  results = {}

  def __init__(self):
    with open(self.teams_file, 'r') as yaml_in:
      try:
          teams = yaml.load(yaml_in, Loader=yaml.FullLoader)
          self.teams = teams[self.league_key]
          self.team_keys = dict(zip(self.teams.values(), self.teams.keys()))
      except yaml.YAMLError as yamlException:
        raise yamlException

  # override start_request to use an own dict instead of start_urls
  def start_requests(self):
    for key, url in self.teams.items():
      yield Request(url, self.parse)

  def parse(self, response):
    # get the team's name
    team = str(response.xpath('//h1/text()').get()).strip()

    # select coach
    headCoach = response.xpath("//text()[contains(., 'Head Coach')]/following::a[1]/text()").extract()
    # select assistant coach
    assistantCoach = response.xpath("//text()[contains(., 'Asst. Coach')]/following::a[1]/text()").extract()

    # set a title
    content = "- " + str(team) + " -\n\n"

    current_team_key = ""

    people = []
    # for players in response.css('table.roster tbody tr'):
    # for players in response.xpath('//table[contains(@class, "SortTable_table__")]/tbody/tr/td/div[contains(@class, "Roster_player__")]'):
    for index, htmlContent in enumerate(response.xpath('//div[contains(@class, "Roster_player__")]')):
      current_team_key = self.team_keys[response.url]
      number = str(htmlContent.xpath('ancestor::tr/td[2]/text()').get()).strip()
      number = number.replace('#', '')

      name = str(htmlContent.xpath('a/text()').get()).strip()
      # remove any hints on the player's name
      name = str(re.sub('\(.*\)', '', name)).strip()
      # number might not be certain, so we set at least 'something'
      if number != 'None' and name != 'None':
        peopleStr = "%s%s\t-%s- %s (%s)\n" % (current_team_key, number, number, name, team)
        people.insert(int(number), peopleStr)
      if number == 'None' and name != 'None':
        peopleStr = "%s%s\t-%s- %s (%s)\n" % (current_team_key, index, index, name, team)
        people.insert(index, peopleStr)

    # sorting players by index/number
    # people.sort()

    if headCoach:
      peopleStr = "%s100\t%s (Trainer %s)\n" % (current_team_key, headCoach[0].strip(), team)
      people.insert(100, peopleStr)
    if assistantCoach:
      peopleStr = "%s101\t%s (Co-Trainer %s)\n" % (current_team_key, assistantCoach[0].strip(), team)
      people.insert(101, peopleStr)

    for item in people:
      itemString = str(item)
      content += itemString

    content += "\n\n"
    self.results[self.team_keys[response.url]] = content

  def __del__(self):
    content = ""
    for key in sorted(self.results):
      content += self.results[key]

    with open(self.league_key + '.txt', 'w+') as f:
      f.write(content)