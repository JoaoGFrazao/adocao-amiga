from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class ListAnonRateThrottle(AnonRateThrottle):
    rate = '100/day'
class ListUserRateThrottle(UserRateThrottle):
    rate = '200/day'

class DetailAnonRateThrottle(AnonRateThrottle):
    rate = '150/day'
class DetailUserRateThrottle(UserRateThrottle):   
    rate = '300/day'

class FilterAnonRateThrottle(AnonRateThrottle):
    rate = '150/day'
class FilterUserRateThrottle(UserRateThrottle):   
    rate = '300/day'