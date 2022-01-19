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

    welcome_text = \
        ["is needy and wait's for academic trash talk",
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
