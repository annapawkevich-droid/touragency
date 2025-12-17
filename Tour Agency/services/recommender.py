from models.resort import Resort, SurveyAnswers

class StaticRecommendationService:

    def __init__(self):
        self.resorts = [ #список
            Resort("Шарм-ель-Шейх", "Єгипет",
                   {"sea":10,"mountain":0,"excursion":3,"nature":2,"family":9,"party":6},
                   "☀️ Пляжний рай для родин і відпочинку."),
            Resort("Анталія", "Туреччина",
                   {"sea":9,"mountain":1,"excursion":5,"nature":3,"family":10,"party":5},
                   "🏖️ Комфорт і море, сімейний формат."),
            Resort("Балі", "Індонезія",
                   {"sea":10,"mountain":3,"excursion":5,"nature":9,"family":6,"party":8},
                   "🌴 Серфінг, природа, екзотика."),
            Resort("Буковель", "Україна",
                   {"sea":0,"mountain":10,"excursion":4,"nature":8,"family":7,"party":6},
                   "⛰️ Карпати, гори, лижі, затишок."),
            Resort("Прага", "Чехія",
                   {"sea":0,"mountain":0,"excursion":10,"nature":6,"family":7,"party":5},
                   "🏰 Європейські екскурсії."),
            Resort("Мальдіви", "Мальдіви",
                   {"sea":10,"mountain":0,"excursion":2,"nature":10,"family":8,"party":3},
                   "🌊 Райський відпочинок біля океану."),
            Resort("Токіо", "Японія",
                   {"sea":5,"mountain":2,"excursion":10,"nature":8,"family":5,"party":8},
                   "🗾 Мегаполіс, культура, нічне життя."),
            Resort("Барселона", "Іспанія",
                   {"sea":9,"mountain":2,"excursion":9,"nature":7,"family":7,"party":9},
                   "☀️ Море, архітектура і веселощі."),
        ]

    def recommend_top(self, answers: SurveyAnswers, top_n: int = 3):
        def score(resort: Resort) -> int:
            return sum(resort.profile[k] * getattr(answers, k) for k in resort.profile)
        sorted_resorts = sorted(self.resorts, key=score, reverse=True)
        return sorted_resorts[:top_n]
