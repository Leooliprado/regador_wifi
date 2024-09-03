import smtplib
import email.message




def enviar_email(email_receber, irrigar_hoje, data_irrigacao):  
    corpo_email = f"""
   <!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href='https://fonts.googleapis.com/css?family=Montserrat' rel='stylesheet'>
    <title>WateringCan</title>
</head>

<body style="margin: 0; font-family: 'Montserrat', sans-serif; font-size: 18px;">
    <div style="background: white; color: #ffffff; margin: 0px auto; width: 100%;">
        <div style="margin: 0px auto; padding: 30px 0; height: 95%; width: 100%; max-width: 680px;">
            <div style="text-align: center;">
                <!-- Conteúdo adicional pode ser adicionado aqui -->
            </div>
            <div style="width: 100%; max-width: 680px; margin-bottom: 30px; background-color: #141118; border-radius: 8px;">
                <div style="width: 100%; max-width: 680px; height: 140px; background-color: #DF840B; border-radius: 8px 8px 0 0;">
                    <h2 style="margin: 0; color: white; padding: 60px 40px;">WateringCan</h2>
                </div>
                <div style="padding: 30px 20px;">
                    <p style="margin: 20px 0;">
                       A irrigação foi realizada em <b>{data_irrigacao}</b>.
                    </p>
                    <p style="margin: 20px 0;">
                        Irrigou hoje <b>{irrigar_hoje} vezes</b>.
                    </p>
                    <div style="background: #DF840B; text-align: center; color: white; margin: 0 auto; width: 180px; border-radius: 10px; font-size: 22px; padding: 8px; margin-top: 40px;">
                        <b>Bomba D'água Ligada!</b>
                    </div>
                    <div style="margin-top: 80px;"></div>
                </div>
            </div>
        </div>
    </div>
</body>

</html>
    """

    msg = email.message.Message()
    msg['Subject'] = "WateringCan"
    msg['From'] = ''
    msg['To'] = email_receber
    password = ''

    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Email enviado com sucesso!')
    except Exception as e:
        print(f'Erro ao enviar e-mail: {str(e)}')
    finally:
        s.quit()

