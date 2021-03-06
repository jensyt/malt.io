from handlers.auth import AuthHandler, AuthCallbackHandler, \
                          LoginHandler, LogoutHandler
from handlers.donate import DonateHandler
from handlers.formulas import FormulasHandler
from handlers.index import MainHandler
from handlers.messages import MessagesHandler
from handlers.profile import ProfileHandler
from handlers.recipes import RecipesHandler, RecipeEmbedHandler, \
                             RecipeLikeHandler, RecipeCloneHandler, \
                             RecipeHandler, RecipeXmlHandler, \
                             RecipeHistoryHandler
from handlers.users import UsersHandler, UserHandler, UserFollowHandler, \
                           UsernameCheckHandler

# The following maps regular expressions to specific handlers.
# Matched groups become positional arguments to the handler's methods.
urls = [
    ('/users/(.*?)/recipes/(.*?)/like', RecipeLikeHandler),
    ('/users/(.*?)/recipes/(.*?)/clone', RecipeCloneHandler),
    ('/users/(.*?)/recipes/(.*?)/beerxml', RecipeXmlHandler),
    ('/users/(.*?)/recipes/(.*?)/history', RecipeHistoryHandler),
    ('/users/(.*?)/recipes/(.*?)/history/(.*)', RecipeHandler),
    ('/users/(.*?)/recipes/(.*)', RecipeHandler),
    ('/users/(.*?)/recipes', RecipesHandler),
    ('/users/(.*?)/follow', UserFollowHandler),
    ('/users/(.*)', UserHandler),
    ('/users', UsersHandler),
    ('/username', UsernameCheckHandler),
    ('/recipes', RecipesHandler),
    ('/messages', MessagesHandler),
    ('/profile', ProfileHandler),
    ('/new', RecipeHandler),
    ('/embed/(.*?)/(.*?)', RecipeEmbedHandler),
    ('/homebrew-formulas', FormulasHandler),
    ('/donate', DonateHandler),
    ('/auth/(.*?)/callback', AuthCallbackHandler),
    ('/auth/(.*?)', AuthHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/', MainHandler)
]
