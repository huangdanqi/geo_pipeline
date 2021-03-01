# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 00:34:52 2021

@author: DANQI
"""


import requests
import time 
import xml.dom.minidom
import re
import wget
import tarfile
import shutil
import os
from pathlib import Path


#gse_list=["GSE167334","GSE167089","GSE167037"]
gse_list=["GSE167089","GSE167037"]


def download_gse(gse_list):
    os.makedirs('gse') 

    for gse in gse_list:
        try:
            gse_nnn=gse[:-3]
            gse_nnn=gse_nnn+"nnn"
            url="ftp://ftp.ncbi.nlm.nih.gov/geo/series/"+gse_nnn+"/"+gse+"/miniml/"+gse+"_family.xml.tgz"

            wget.download(url,out='gse')
            try :
                path_gse="./gse/"+gse+"_family.xml.tgz"
                data_folder = Path(path_gse)
                tar = tarfile.open(data_folder)  
                names = tar.getnames()   
                for name in names:  
                    #print(name)
                    tar.extract(name,'gse')  
                tar.close()
            except Exception :
                print('extract wrong')
            
            dirs = os.listdir('gse')
            gse_extract_file_list=[]
            for j in gse_list:
                gse_extract_file=j+"_family.xml"
                gse_extract_file_list.append(gse_extract_file)
                
            
            #gse_extract_file=gse+"_family.xml"
            #gse_extract_file_tgz=gse+"_family.xml.tgz"
            #print(i,gse_extract_file)
            #print(dirs)
            for i in dirs:    
                #print(i)
                #print(gse_extract_file_list)
                if i in gse_extract_file_list :
                    pass
                else:
                    path="./gse"+"/"+i
                    data_folder = Path(path)
                    os.remove(data_folder)
        except:
            print('{},we can not download this gse.\n'.format(gse))
            continue
        
download_gse(gse_list)


def query_raw(text, url="https://bern.korea.ac.kr/plain"):
    try:
        return requests.post(url, data={'sample_text': text}).json()
    except(requests.exceptions.ConnectionError,NameError):
        time.sleep(10)
        return requests.post(url, data={'sample_text': text}).json()

def bern_list(output):
    
    disease=[]
    disease_id=[]
    
    drug=[]
    drug_id=[]
    
    gene=[]
    gene_id=[]
    

    
    if output:
        try:
            
            if output['denotations']:
                
                for i in output['denotations']:
                    if i['obj'] == 'disease':
                                
                        if i['obj']:
                            n=i['span']
                            begin=n['begin']
                            end=n['end']
                            #print(n)
                            name=str(output['text'])[begin:end]
                             
                            id_list=i['id']
                            for j in id_list:
                                if str(j)=='CUI-less':
                                    break
                                else:
                                    id_need=";".join(id_list)
                                    disease_id.append(id_need)
                                    disease.append(name) 
          
                    if i['obj'] == 'drug':
                        if i['obj']:
                            n=i['span']
                            begin=n['begin']
                            end=n['end']
                            #print(n)
                            name=str(output['text'])[begin:end]
                    
                            id_list=i['id']
                            for j in id_list:
                                if str(j)=='CUI-less':
                                    break
                                else:
                                    id_need=";".join(id_list)
                                    drug_id.append(id_need)
                                    drug.append(name) 
                            #species.append(name)
                    
                    if i['obj'] == 'gene':
                        if i['obj']:
                            n=i['span']
                            begin=n['begin']
                            end=n['end']
                            #print(n)
                            name=str(output['text'])[begin:end]
                            #gene.append(name)
                            id_list=i['id']
                            for j in id_list:
                                if str(j)=='CUI-less':
                                    break
                                else:
                                    id_need=";".join(id_list)
                                    gene_id.append(id_need)
                                    gene.append(name) 
            if disease:
                disease_set=set(disease)
                disease_str='|'.join(disease_set)
                disease_id_set=set(disease_id)
                disease_id_str='|'.join(disease_id_set)
                
                # for i in disease_set:
                #     disease_str=disease_str+i+','
                #     disease_str=disease_str[:-1]    
            else:
                disease_str='null'
                disease_id_str='null'
                
            if drug:
                drug_set=set(drug)
                drug_str='|'.join(drug_set)
                drug_id=set(drug_id)
                drug_id_str='|'.join(drug_id)       
            else:
                drug_str='null'
                drug_id_str='null'
                
            if gene:
                gene_set=set(gene)
                gene_str='|'.join(gene_set)
                gene_id=set(gene_id)
                gene_id_str='|'.join(gene_id)
            else:
                gene_str='null'
                gene_id_str='null'
        except:
            disease_str=disease_id_str=drug_str=drug_id_str=gene_str=gene_id_str='null'
            
    else:
        disease_str=disease_id_str=drug_str=drug_id_str=gene_str=gene_id_str='null'
        
    return disease_str,disease_id_str,drug_str,drug_id_str,gene_str,gene_id_str 

def pipeline():
    with open('zrb_pipeline_bern_result',"a",encoding='utf-8') as out:
        title=['text','gsm','cell line','organism','cell type','method','source name','tissue','treatment','disease','bern_zrb_disease','bern_zrb_disease_id','bern_zrb_drug','bern_zrb_drug_id','bern_zrb_gene','bern_zrb_gene_id']      
        title_line="\t".join(title)
        out.write(title_line)
        out.write('\n')
    file_list=[]
    file_list=os.listdir('gse')
   # print(file_list)

    for i_file in file_list:

        file_path = os.path.join(os.path.abspath('.'), 'gse')
        file_path_need = os.path.join( file_path,i_file)

        
       
        dom=xml.dom.minidom.parse(file_path_need)
        def move_break(need_list):
            for i in range(len(need_list)):
                need_list[i]=re.sub("\n","",need_list[i])
                need_list[i]=re.sub("\s+"," ",need_list[i])
            return need_list    
        Platform = dom.getElementsByTagName("Platform")

        p_technology_list=[]


        for i_p in range(Platform.length):

      
            try:
                p_technology=dom.getElementsByTagName("Platform")[i_p].getElementsByTagName("Technology")[0].childNodes[0].data
                p_technology_list.append(p_technology)
               
            except:
                p_technology_list.append("null")
            
        
        
        p_technology_list=move_break(p_technology_list)
        p_technology_all=",".join(str(x) for x in p_technology_list)




        #extract sample tags
        sample=dom.getElementsByTagName("Sample")
       #sample_list=[]
        #sample_data_list=[]
        sample_char_list=[]
        #sample_table_list=[]
        for i_s in range(sample.length):
            output_list=[]
            try:
                s_number=sample[i_s].getAttribute("iid")
                
            except:
                s_number="null"
                
            try:
                s_title=sample[i_s].getElementsByTagName("Title")[0].childNodes[0].data
            except:
                s_title=sample[i_s]="null"
            

            try:
                s_source=sample[i_s].getElementsByTagName("Source")[0].childNodes[0].data
            except:
                s_source="null"
            
            try:
                s_organism=sample[i_s].getElementsByTagName("Organism")[0].childNodes[0].data
            except:
                s_organism="null"
                
            #会出现换行符
            
            try:
                s_Last_Update_Date=sample[i_s].getElementsByTagName("Last-Update-Date")[0].childNodes[0].data
                
            except:
                 s_Last_Update_Date="null"     
            
            try:
                s_Release_Date=sample[i_s].getElementsByTagName("Release-Date")[0].childNodes[0].data
                
            except:
                s_Release_Date="null"         
                 
            #SAGE 特有的
            try:
                s_anchor=sample[i_s].getElementsByTagName("Anchor")[0].childNodes[0].data
                s_anchor="(SAGE_anchor)"+s_anchor
            except:
                s_anchor="(SAGE_anchor)null"
            
            try:
                s_type=sample[i_s].getElementsByTagName("Type")[0].childNodes[0].data
                s_type="(SAGE_type)"+s_type
            except:
                s_type="(SAGE_type)null"
            
            try:
                s_tag_count=sample[i_s].getElementsByTagName("Tag-Count")[0].childNodes[0].data
                s_tag_count="(SAGE_count)"+s_tag_count
            except:
                s_tag_count="(SAGE_count)null"
            
            try:
                s_tag_length=sample[i_s].getElementsByTagName("Tag-Length")[0].childNodes[0].data
                s_tag_length="(SAGE_len)"+s_tag_length
            except:
                s_tag_length="(SAGE_len)null"
                
    
            
            #把characteristic放在最后，是因为characteristic对每个GSE是不同的
            chr_str=''
            try:
                s_char_array=sample[i_s].getElementsByTagName("Characteristics")
                for i in range(s_char_array.length):
                    s_char_tag=s_char_array[i].getAttribute("tag")
                    
                    #text里面有换行符
                    s_char_text=s_char_array[i].childNodes[0].data
                    if not s_char_tag:
                        s_char_tag='characteristics'
                    chr_str=chr_str+"'"+s_char_tag+"'"+":"+"'"+s_char_text+"'"+","
                    s_char="[char]({}){}".format(s_char_tag,s_char_text)
                    sample_char_list.append(s_char)
                #s_char_need="*#*#*#".join(sample_char_list)   
                sample_char_list=[]
                
            except:
                pass
                #s_char_need="null"
            
            chr_str=re.sub(r'\n', '', chr_str)  
            chr_str=re.sub(r'\s+', ' ', chr_str)
            output_col_1="{"+chr_str+"'organism':"+"'"+s_organism+"'"+",'source name':"+"'"+s_source+"'"+", 'title':"+"'"+s_title+"'"+", 'last update date':"+"'"+s_Last_Update_Date+"'"+", 'release date': "+"'"+s_Release_Date+"'"+", 'method': "+"'"+p_technology_all+"'"+"}"
            output_list.append(output_col_1)
            output_list.append(s_number)
            #output_list.append(virus_name)
            
            
            #extract characteristic alone
            # line_list=line.split('\t')
            # line_text=line_list[0]
            
            #line_dict={}
            line_text_list=output_col_1.split(',')
            line_dict={}
            match_list=['cell line','organism','cell type','method','source name','tissue','disease','treatment']
            for i in line_text_list:
                i=re.sub("'", "", i)
                i=re.sub(r"\{", "", i)
                i=re.sub(r"\}", "", i)
                i=re.sub(r'"', "", i)
                i=i.strip()
                dcit_list=i.split(':')
                #line_dict[str(dcit_list[0])]=str(dcit_list[1])
                
                dcit_list[0]=re.sub("'", "", dcit_list[0])
                dcit_list[0]=re.sub(r"\{", "", dcit_list[0])
                dcit_list[0]=re.sub(r"\}", "", dcit_list[0])
                dcit_list[0]=re.sub(r'"', "", dcit_list[0])
                dcit_list[0]=str(dcit_list[0]).strip()
                try:
                    line_dict[str(dcit_list[0])]=str(dcit_list[1])
                except:
                    line_dict[str(dcit_list[0])]='null'
            for i in match_list:
                if i in line_dict.keys():
                    line_dict[i]=str(line_dict[i]).strip()
                    output_list.append(str(line_dict[i]))
                else:
                    output_list.append('null')
    
            
                
            
        #换行符和多个空格的问题
            #sample_single=s_number+"*#*#*#"+s_title+"*#*#*#"+s_channel+"*#*#*#"+s_source+"*#*#*#"+s_organism+"*#*#*#"+s_treatment+"*#*#*#"+s_growth+"*#*#*#"+s_molecule+"*#*#*#"+s_extract+"*#*#*#"+s_label+"*#*#*#"+s_data_processing+"*#*#*#"+s_description+"*#*#*#"+s_platform_ref+"*#*#*#"+s_Last_Update_Date+"*#*#*#"+s_Release_Date+"*#*#*#"+s_anchor+"*#*#*#"+s_type+"*#*#*#"+s_tag_count+"*#*#*#"+s_tag_length+"*#*#*#"+s_char_need
            zrb_bern=query_raw(output_col_1)
            #print(sample_list_all)
            #hdq_bern=query_raw(sample_single)
            zrb_disease_str,zrb_disease_id_str,zrb_drug_str,zrb_drug_id_str,zrb_gene_str,zrb_gene_id_str=bern_list(zrb_bern)
            zrb_bern_list=[zrb_disease_str,zrb_disease_id_str,zrb_drug_str,zrb_drug_id_str,zrb_gene_str,zrb_gene_id_str]
            for i in zrb_bern_list:
                output_list.append(str(i))
            
            # hdq_disease_str,hdq_disease_id_str,hdq_drug_str,hdq_drug_id_str,hdq_gene_str,hdq_gene_id_str=bern_list(hdq_bern)   
            # hdq_bern_list=[hdq_disease_str,hdq_disease_id_str,hdq_drug_str,hdq_drug_id_str,hdq_gene_str,hdq_gene_id_str]
            # for j in hdq_bern_list:
            #     output_list.append(str(j))
                #for i in output_list :
            
            line='\t'.join(output_list)
            line=line+'\n'
            with open('zrb_pipeline_bern_result',"a",encoding='utf-8') as out:
                out.write(line)

pipeline()

#删除文件夹
shutil.rmtree('gse')

    
    