class Conf:
    ec2_instance_id = 'i-07baa970d1c82bb08'

    channel_welcome = 752618408939487292
    channel_status = 852114543759982592
    massage_status = 883458320290152528

    mc_server_aternos1 = "ratius99.aternos.me"
    mc_server_amazon = "3.125.141.61"

    time_delete_random = 60
    time_check_mcserver = 10
    time_check_mcserver_seconds = 30
    time_do_tasks = 30
    count_check_aws_mcserver = 10

    activity_name_basic = " in der Cloud! ☁"

    welcome_text = [
        "is needy and wait's for academic trash talk",
        "iws needy awnd wait's fow academic twash tawk",
        "is lonely and want's to talk",
        "is waiting for you",
        "is sitting alone here",
        "wants to procrastinate",
        "is dying of boredom",
        "has a quarterlife-crisis",
        "is plotting to overthrow the government",
        "is hiding a bomb below their desk"
        ]
    
    quotes = [       
        "\"It’s time for you to look inward and start asking yourself the big question: who are you and what do you want?\" ~Iroh",
        "\"Be careful what you wish for, Admiral. History is not always kind to its subjects.\" ~Iroh",
        "\"You are going through a metamorphosis, my nephew. It will not be a pleasant experience but when you come out of it. You will be the beautiful prince you were always meant to be.\" ~Iroh",
        "\"Many things that seem threatening in the dark become welcoming when we shine light on them.\" ~Iroh",
        "\"Is it your own destiny? Or is it a destiny someone else has tried to force on you?\" ~Iroh",
        "\"You have light and peace inside of you. If you let it out, you can change the world around you.\" ~Iroh",
        "\"Even in the material world, you will find that if you look for the light, you can often find it. But if you look for the dark, that is all you will ever see.\" ~Iroh",
        "\"Failure is only the opportunity to begin again. Only this time, more wisely.\" ~Iroh",
        "\"Good times become good memories, but bad times become good lessons.\" ~Iroh",
        "\"You are not the man you used to be. You are stronger and wiser and freer than you ever used to be. And now you have come at the crossroads of the destiny. It’s time for you to choose. It’s time for you to choose good.\" ~Iroh",
        "\"Follow your passion and life will reward you.\" ~Iroh",
        "\"At my age, there is really only one big surprise left, and I’d just as soon leave it a mystery.\" ~Iroh",
        "\"You must look within yourself to save yourself from your other self. Only then will your true self reveal itself.\" ~Iroh",
        "\"It is important to draw wisdom from different places. If you take it from only one place it becomes rigid and stale.\" ~Iroh",
        "\"Sometimes life is like this dark tunnel, you can’t always see the light at the end of the tunnel, but if you just keep moving, you will come to a better place.\" ~Iroh",
        "\"Life happens wherever you are, whether you make it or not.\" ~Iroh",
        "\"Destiny is a funny thing. You never know how things are going to work out. But if you keep an open mind and an open heart, I promise you will find your own destiny someday.\" ~Iroh",
        "\"It is usually best to admit mistakes when they occur, and to seek to restore honor.\" ~Iroh",
        "\"While it is always best to believe in one’s self, a little help from others can be a great blessing.\" ~Iroh",
        "\"Sometimes the best way to solve your own problems is to help someone else.\" ~Iroh",
        "\"Protection and power are overrated. I think you are very wise to choose happiness and love.\" ~Iroh",
        "\"There’s nothing wrong with a life of peace and prosperity. I suggest you think about what it is that you want from your life, and why.\" ~Iroh",
        "\"I was never angry with you. I was sad, because I was afraid you’d lost your way.\" ~Iroh",
        "\"Pride is not the opposite of shame, but it’s source. True humility is the only antidote to shame.\" ~Iroh",
        "\"In the darkest times, hope is something you give yourself. That is the meaning of inner strength.\" ~Iroh",
        "\"You must never give into despair. Allow yourself to slip down that road and you surrender to your lowest instincts.\" ~Iroh",
        "\"Understanding others, the other elements, the other nations, will help you become whole.\" ~Iroh",
        "\"It is the combination of the four elements in one person that makes the Avatar so powerful. But it can make you more powerful too.\" ~Iroh",
        "\"Who knew floating on a piece of driftwood for three weeks, with no food or water, and sea vultures waiting to pluck out your liver, could make one so tense!\" ~Iroh",
        "\"There is nothing wrong with letting people who love you, help you. Not that I love you. I just met you.\" ~Iroh",
        "\"I know you’re not supposed to cry over spilled tea, but it’s just so sad!\" ~Iroh",
        "\"Who would have thought that, after all these years, I would return to the scene of my greatest military disgrace…as a tourist!\" ~Iroh",
        "\"More tea, please!\" ~Iroh",
        "\"Zuko, it’s time we had a talk…about your hair. It’s gone too far!\" ~Iroh",
        "\"Ick! This tea is nothing more than hot leaf juice!\" ~Iroh",
        "\"You’re looking at the rare white dragon bush. Its leaves make a tea so delicious it’s heartbreaking! That, or it’s the white jade bush, which is poisonous.\" ~Iroh",
        "\"Sick of tea? That’s like being sick of breathing!\" ~Iroh",
        "\"I always tried to tell you that Pai Sho is more than just a game.\" ~Iroh",
        "\"The only thing better than finding something you are looking for is finding something you weren’t looking for at a great bargain!\" ~Iroh",
        "\"So I was thinking about names for my new tea shop… how about… the Jasmine Dragon? It’s dramatic, poetic… has a nice ring to it.\" ~Iroh",
        "\"It’s a lovely night for a walk. Why don’t you join me? It would clear your head. Or, just stay in your room and sit in the dark. Whatever makes you happy.\" ~Iroh",
        "\"You should know this is not a natural sickness. But that shouldn’t stop you from enjoying tea.\" ~Iroh",
        "\"You sound like my nephew. Always thinking you need to do things on your own without anyone’s support.\" ~Iroh",
        ]
    
    @staticmethod
    def mcserver_controller_message(aws_ip, aws_text):
        return "" \
               "--> Kontrolliere hier mit Reaktionen den tEsTOot:\n" \
               "   - Starte (:white_check_mark:) und stoppe (:x:) den Amazon Minecraftserver.\n" \
               "\n" \
               "--> Serverstatus: \n" \
               f"   - Amazon 18.1 (minecraft.konziiis.de)*: {aws_text}\n" \
               "   - Aternos 17.1 (ratius99.aternos.me): siehe Bot-Status\n" \
               "   - Aternos 16.X (Konziiis.aternos.me): siehe <#781561552300933182>  \n\n" \
               f"*Alternative IP: {aws_ip}"

    colors = [0xFFE4E1, 0x00FF7F, 0xD8BFD8, 0xDC143C, 0xFF4500, 0xDEB887, 0xADFF2F, 0x800000,
              0x4682B4, 0x006400, 0x808080, 0xA0522D, 0xF08080, 0xC71585, 0xFFB6C1, 0x00CED1]
