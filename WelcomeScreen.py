import random
import types
import Author_ASCII_art

def printWelcomeScreen():
    # Get a list of all function names in the Author_ASCII_art module
    author_functions = [f for f in dir(Author_ASCII_art) if callable(getattr(Author_ASCII_art, f)) and not f.startswith("__")]
    
    # Select a random function name from the list
    function_name = random.choice(author_functions)

    # Get the function object associated with the string name
    printAuthor = getattr(Author_ASCII_art, function_name)

    # Call the function
    printAuthor()

    # # Test START ==============
    # for function_name  in author_functions:
    #     print(function_name)
    #     # Get the function object associated with the string name
    #     printAuthor = getattr(Author_ASCII_art, function_name)
    #     # Call the function
    #     printAuthor()
    # # Test END   ==============

    # Print App Name
    printAppName()

    # Print Description
    print(r"""
    Welcome to Chat GPT File Navigator Pro! The ultimate solution for quick and efficient text copying from multiple files.
    
        Press any control key to continue ...
    """)
#end

## ====================================== Software Application name ASCII art ======================================

def printAppName():
     print(r"""
           _____   _               _        _____   _____    _______     _______                   _                                     
          / ____| | |             | |      / ____| |  __ \  |__   __|   |__   __|                 | |                                    
         | |  __  | |__     __ _  | |_    | |  __  | |__) |    | |         | |      ___     ___   | |                                    
         | | |_ | | '_ \   / _` | | __|   | | |_ | |  ___/     | |         | |     / _ \   / _ \  | |                                    
         | |__| | | | | | | (_| | | |_    | |__| | | |         | |         | |    | (_) | | (_) | | |                                    
          \_____| |_| |_|  \__,_|  \__|    \_____| |_|         |_|         |_|     \___/   \___/  |_|                                    
                                                                                                                                         
                                                                                                                                         
  __  __           _   _     _                ______   _   _             _____                             _______                 _     
 |  \/  |         | | | |   (_)              |  ____| (_) | |           / ____|                           |__   __|               | |    
 | \  / |  _   _  | | | |_   _     ______    | |__     _  | |   ___    | |        ___    _ __    _   _       | |      ___  __  __ | |_   
 | |\/| | | | | | | | | __| | |   |______|   |  __|   | | | |  / _ \   | |       / _ \  | '_ \  | | | |      | |     / _ \ \ \/ / | __|  
 | |  | | | |_| | | | | |_  | |              | |      | | | | |  __/   | |____  | (_) | | |_) | | |_| |      | |    |  __/  >  <  | |_   
 |_|  |_|  \__,_| |_|  \__| |_|              |_|      |_| |_|  \___|    \_____|  \___/  | .__/   \__, |      |_|     \___| /_/\_\  \__|  
                                                                                        | |       __/ |                                  
                                                                                        |_|      |___/                                   
    """)
#end

def printAppName_big():
    print(r"""                                                                                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                                                                     
                            GGGGGGGGGGGGGhhhhhhh                                        tttt                       GGGGGGGGGGGGGPPPPPPPPPPPPPPPPP   TTTTTTTTTTTTTTTTTTTTTTT     TTTTTTTTTTTTTTTTTTTTTTT                                  lllllll                                                                                                                     
                         GGG::::::::::::Gh:::::h                                     ttt:::t                    GGG::::::::::::GP::::::::::::::::P  T:::::::::::::::::::::T     T:::::::::::::::::::::T                                  l:::::l                                                                                                                     
                       GG:::::::::::::::Gh:::::h                                     t:::::t                  GG:::::::::::::::GP::::::PPPPPP:::::P T:::::::::::::::::::::T     T:::::::::::::::::::::T                                  l:::::l                                                                                                                     
                      G:::::GGGGGGGG::::Gh:::::h                                     t:::::t                 G:::::GGGGGGGG::::GPP:::::P     P:::::PT:::::TT:::::::TT:::::T     T:::::TT:::::::TT:::::T                                  l:::::l                                                                                                                     
                     G:::::G       GGGGGG h::::h hhhhh         aaaaaaaaaaaaa   ttttttt:::::ttttttt          G:::::G       GGGGGG  P::::P     P:::::PTTTTTT  T:::::T  TTTTTT     TTTTTT  T:::::T  TTTTTT   ooooooooooo      ooooooooooo    l::::l                                                                                                                     
                    G:::::G               h::::hh:::::hhh      a::::::::::::a  t:::::::::::::::::t         G:::::G                P::::P     P:::::P        T:::::T                     T:::::T         oo:::::::::::oo  oo:::::::::::oo  l::::l                                                                                                                     
                    G:::::G               h::::::::::::::hh    aaaaaaaaa:::::a t:::::::::::::::::t         G:::::G                P::::PPPPPP:::::P         T:::::T                     T:::::T        o:::::::::::::::oo:::::::::::::::o l::::l                                                                                                                     
                    G:::::G    GGGGGGGGGG h:::::::hhh::::::h            a::::a tttttt:::::::tttttt         G:::::G    GGGGGGGGGG  P:::::::::::::PP          T:::::T                     T:::::T        o:::::ooooo:::::oo:::::ooooo:::::o l::::l                                                                                                                     
                    G:::::G    G::::::::G h::::::h   h::::::h    aaaaaaa:::::a       t:::::t               G:::::G    G::::::::G  P::::PPPPPPPPP            T:::::T                     T:::::T        o::::o     o::::oo::::o     o::::o l::::l                                                                                                                     
                    G:::::G    GGGGG::::G h:::::h     h:::::h  aa::::::::::::a       t:::::t               G:::::G    GGGGG::::G  P::::P                    T:::::T                     T:::::T        o::::o     o::::oo::::o     o::::o l::::l                                                                                                                     
                    G:::::G        G::::G h:::::h     h:::::h a::::aaaa::::::a       t:::::t               G:::::G        G::::G  P::::P                    T:::::T                     T:::::T        o::::o     o::::oo::::o     o::::o l::::l                                                                                                                     
                     G:::::G       G::::G h:::::h     h:::::ha::::a    a:::::a       t:::::t    tttttt      G:::::G       G::::G  P::::P                    T:::::T                     T:::::T        o::::o     o::::oo::::o     o::::o l::::l                                                                                                                     
                      G:::::GGGGGGGG::::G h:::::h     h:::::ha::::a    a:::::a       t::::::tttt:::::t       G:::::GGGGGGGG::::GPP::::::PP                TT:::::::TT                 TT:::::::TT      o:::::ooooo:::::oo:::::ooooo:::::ol::::::l                                                                                                                    
                       GG:::::::::::::::G h:::::h     h:::::ha:::::aaaa::::::a       tt::::::::::::::t        GG:::::::::::::::GP::::::::P                T:::::::::T                 T:::::::::T      o:::::::::::::::oo:::::::::::::::ol::::::l                                                                                                                    
                         GGG::::::GGG:::G h:::::h     h:::::h a::::::::::aa:::a        tt:::::::::::tt          GGG::::::GGG:::GP::::::::P                T:::::::::T                 T:::::::::T       oo:::::::::::oo  oo:::::::::::oo l::::::l                                                                                                                    
                            GGGGGG   GGGG hhhhhhh     hhhhhhh  aaaaaaaaaa  aaaa          ttttttttttt               GGGGGG   GGGGPPPPPPPPPP                TTTTTTTTTTT                 TTTTTTTTTTT         ooooooooooo      ooooooooooo   llllllll                                                                                                                    
#end
                                                                                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                                                                     
MMMMMMMM               MMMMMMMM                  lllllll          tttt            iiii                             FFFFFFFFFFFFFFFFFFFFFF  iiii  lllllll                                  CCCCCCCCCCCCC                                                                   TTTTTTTTTTTTTTTTTTTTTTT                                                 tttt               
M:::::::M             M:::::::M                  l:::::l       ttt:::t           i::::i                            F::::::::::::::::::::F i::::i l:::::l                               CCC::::::::::::C                                                                   T:::::::::::::::::::::T                                              ttt:::t               
M::::::::M           M::::::::M                  l:::::l       t:::::t            iiii                             F::::::::::::::::::::F  iiii  l:::::l                             CC:::::::::::::::C                                                                   T:::::::::::::::::::::T                                              t:::::t               
M:::::::::M         M:::::::::M                  l:::::l       t:::::t                                             FF::::::FFFFFFFFF::::F        l:::::l                            C:::::CCCCCCCC::::C                                                                   T:::::TT:::::::TT:::::T                                              t:::::t               
M::::::::::M       M::::::::::Muuuuuu    uuuuuu   l::::l ttttttt:::::ttttttt    iiiiiii                              F:::::F       FFFFFFiiiiiii  l::::l     eeeeeeeeeeee          C:::::C       CCCCCC   ooooooooooo   ppppp   ppppppppp   yyyyyyy           yyyyyyy     TTTTTT  T:::::T  TTTTTT    eeeeeeeeeeee    xxxxxxx      xxxxxxxttttttt:::::ttttttt         
M:::::::::::M     M:::::::::::Mu::::u    u::::u   l::::l t:::::::::::::::::t    i:::::i                              F:::::F             i:::::i  l::::l   ee::::::::::::ee       C:::::C               oo:::::::::::oo p::::ppp:::::::::p   y:::::y         y:::::y              T:::::T          ee::::::::::::ee   x:::::x    x:::::x t:::::::::::::::::t         
M:::::::M::::M   M::::M:::::::Mu::::u    u::::u   l::::l t:::::::::::::::::t     i::::i                              F::::::FFFFFFFFFF    i::::i  l::::l  e::::::eeeee:::::ee     C:::::C              o:::::::::::::::op:::::::::::::::::p   y:::::y       y:::::y               T:::::T         e::::::eeeee:::::ee  x:::::x  x:::::x  t:::::::::::::::::t         
M::::::M M::::M M::::M M::::::Mu::::u    u::::u   l::::l tttttt:::::::tttttt     i::::i       ---------------        F:::::::::::::::F    i::::i  l::::l e::::::e     e:::::e     C:::::C              o:::::ooooo:::::opp::::::ppppp::::::p   y:::::y     y:::::y                T:::::T        e::::::e     e:::::e   x:::::xx:::::x   tttttt:::::::tttttt         
M::::::M  M::::M::::M  M::::::Mu::::u    u::::u   l::::l       t:::::t           i::::i       -:::::::::::::-        F:::::::::::::::F    i::::i  l::::l e:::::::eeeee::::::e     C:::::C              o::::o     o::::o p:::::p     p:::::p    y:::::y   y:::::y                 T:::::T        e:::::::eeeee::::::e    x::::::::::x          t:::::t               
M::::::M   M:::::::M   M::::::Mu::::u    u::::u   l::::l       t:::::t           i::::i       ---------------        F::::::FFFFFFFFFF    i::::i  l::::l e:::::::::::::::::e      C:::::C              o::::o     o::::o p:::::p     p:::::p     y:::::y y:::::y                  T:::::T        e:::::::::::::::::e      x::::::::x           t:::::t               
M::::::M    M:::::M    M::::::Mu::::u    u::::u   l::::l       t:::::t           i::::i                              F:::::F              i::::i  l::::l e::::::eeeeeeeeeee       C:::::C              o::::o     o::::o p:::::p     p:::::p      y:::::y:::::y                   T:::::T        e::::::eeeeeeeeeee       x::::::::x           t:::::t               
M::::::M     MMMMM     M::::::Mu:::::uuuu:::::u   l::::l       t:::::t    tttttt i::::i                              F:::::F              i::::i  l::::l e:::::::e                 C:::::C       CCCCCCo::::o     o::::o p:::::p    p::::::p       y:::::::::y                    T:::::T        e:::::::e               x::::::::::x          t:::::t    tttttt     
M::::::M               M::::::Mu:::::::::::::::uul::::::l      t::::::tttt:::::ti::::::i                           FF:::::::FF           i::::::il::::::le::::::::e                 C:::::CCCCCCCC::::Co:::::ooooo:::::o p:::::ppppp:::::::p        y:::::::y                   TT:::::::TT      e::::::::e             x:::::xx:::::x         t::::::tttt:::::t     
M::::::M               M::::::M u:::::::::::::::ul::::::l      tt::::::::::::::ti::::::i                           F::::::::FF           i::::::il::::::l e::::::::eeeeeeee          CC:::::::::::::::Co:::::::::::::::o p::::::::::::::::p          y:::::y                    T:::::::::T       e::::::::eeeeeeee    x:::::x  x:::::x        tt::::::::::::::t     
M::::::M               M::::::M  uu::::::::uu:::ul::::::l        tt:::::::::::tti::::::i                           F::::::::FF           i::::::il::::::l  ee:::::::::::::e            CCC::::::::::::C oo:::::::::::oo  p::::::::::::::pp          y:::::y                     T:::::::::T        ee:::::::::::::e   x:::::x    x:::::x         tt:::::::::::tt     
MMMMMMMM               MMMMMMMM    uuuuuuuu  uuuullllllll          ttttttttttt  iiiiiiii                           FFFFFFFFFFF           iiiiiiiillllllll    eeeeeeeeeeeeee               CCCCCCCCCCCCC   ooooooooooo    p::::::pppppppp           y:::::y                      TTTTTTTTTTT          eeeeeeeeeeeeee  xxxxxxx      xxxxxxx          ttttttttttt       
                                                                                                                                                                                                                         p:::::p                  y:::::y                                                                                                            
                                                                                                                                                                                                                         p:::::p                 y:::::y                                                                                                             
                                                                                                                                                                                                                        p:::::::p               y:::::y                                                                                                              
                                                                                                                                                                                                                        p:::::::p              y:::::y                                                                                                               
                                                                                                                                                                                                                        p:::::::p             yyyyyyy                                                                                                                
                                                                                                                                                                                                                        ppppppppp                                                                                                                                    
    """)                                                                                                                                                                                                                                                                                                                                                                    
