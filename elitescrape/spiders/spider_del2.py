from elitescrape.spiders.elitespider import EliteSpider

class Del2Spider(EliteSpider):
  name = "elite_del2"
  league_key = 'del2'
  teams_file = "teams/del2.yaml"

  def __init__(self):
    super(Del2Spider, self).__init__()