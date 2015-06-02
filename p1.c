//Librerias
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <string.h>
#include <math.h>

//estructuras
/*struct palabra{
	char pal[20];
};typedef struct palabra PAL;*/
struct nodo{
	char pal[20];
	struct nodo *sig;
};typedef struct nodo NODO;
struct compuesta{
	NODO *ini,*fin,*aux;
};typedef struct compuesta COM;

int main(){
	int potencia, tama, es, i, j, k=1,cont=0, ces,cont2;
	char palab[20],solu[10];
	FILE *archivo; 
	do{
		do{
			system("cls");
			cont2=0;
			printf("\ncuantos experimentos simples tendra su experimento compuesto?\n");
			scanf("%s",&solu);
			tama=strlen(solu);
			for(i=0;i<tama;i++){
				if(solu[i]=='1'||solu[i]=='2'||solu[i]=='3'||solu[i]=='4'||solu[i]=='5'||solu[i]=='6'||solu[i]=='7'||solu[i]=='8'||solu[i]=='9'||solu[i]=='0')
					cont2++;
			}
		}while(cont2!=tama);
		es=atoi(solu);
	}while(es<2);
	ces=es;
	int resul[es];
	for(j=0;j<es;j++){
		do{
			system("cls");
			cont2=0;
			printf("\ncuantos resutados tiene el experiento %d\n",j+1);
			scanf("%s",&solu);
			tama=strlen(solu);
			for(i=0;i<tama;i++){
				if(solu[i]=='1'||solu[i]=='2'||solu[i]=='3'||solu[i]=='4'||solu[i]=='5'||solu[i]=='6'||solu[i]=='7'||solu[i]=='8'||solu[i]=='9'||solu[i]=='0')
					cont2++;
			}
		}while(cont2!=tama);
		resul[j]=atoi(solu);
	}
	COM compuesta[es];
	int con[es],con2[es];
	for(i=0;i<es;i++){
		con2[i]=0;
	}
	con[es-1]=1;
	for(i=0;i<es;i++){
		compuesta[i].ini=NULL;
		compuesta[i].ini=NULL;
	}
	for(i=0;i<es;i++){
		for(j=0;j<resul[i];j++){
			compuesta[i].aux=(NODO*)malloc(sizeof(NODO)*1);
			if(compuesta[i].ini==NULL){
				compuesta[i].ini=compuesta[i].aux;
				compuesta[i].fin=compuesta[i].aux;
				compuesta[i].fin->sig=NULL;
			}
			else{
				compuesta[i].fin->sig=compuesta[i].aux;
				compuesta[i].fin=compuesta[i].aux;
			}
			printf("\nporfavor ingrese la plabra %d de el conjunto %d",j+1,i+1);
			scanf("%s",&compuesta[i].aux->pal);	
		}
	}
	tama=0;
	for(j=0;j<es-1;j++){
		for(i=ces-1;i>tama;i--){
			k=k*resul[i];
		}
		con[j]=k;
		k=1;
		tama++;
	}
	for(i=0;i<es;i++){
		k=k*resul[i];
	}
	printf("el valor de k es: %d",k);
	for(i=0;i<es;i++){
		compuesta[i].aux=compuesta[i].ini;
	}
	archivo = fopen("salida.txt", "w");
	do{
		cont++;
		fprintf(archivo,"\n%d\t",cont);
		for(i=0;i<es;i++){
			fprintf(archivo,"%s ",compuesta[i].aux->pal);
			if(con2[i]==con[i]-1){
				compuesta[i].aux=compuesta[i].aux->sig;
				if(compuesta[i].aux==NULL){
					compuesta[i].aux=compuesta[i].ini;
				}
				con2[i]=0;
			}
			else 
				con2[i]++;
		}
	}while(cont!=k);
	fclose(archivo);
	system("salida.txt");
	for(i=0;i<es;i++){
		do{
		compuesta[i].aux=compuesta[i].ini;
		compuesta[i].ini=compuesta[i].ini->sig;
		free(compuesta[i].aux);
		}while(compuesta[i].ini!=NULL);
	}
	
	//compuesta[0].aux=(NODO*)malloc(sizeof(NODO)*1);
	
	
}

