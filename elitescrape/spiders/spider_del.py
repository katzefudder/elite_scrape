from elitescrape.spiders.elitespider import EliteSpider

class DelSpider(EliteSpider):
  name = "elite_del"
  league_key = 'del'
  teams_file = "teams/del.yaml"

  def __init__(self):
    super(DelSpider, self).__init__()

