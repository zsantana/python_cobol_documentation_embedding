# Sistema Bancário - Processamento de Transações

Este documento descreve jobs JCL para processamento de transações bancárias com diferentes tipos de programas.

## Job de Processamento Diário

```jcl
//BANCOTX  JOB (BANK001),'PROC TRANSACOES',CLASS=A,MSGCLASS=X,
//         NOTIFY=&SYSUID
//JOBLIB   DD   DSN=BANCO.PROD.LOADLIB,DISP=SHR
//         DD   DSN=SYS1.DB2.DSNLOAD,DISP=SHR

//VALIDA   EXEC PGM=TXVALIDA
//SYSPRINT DD   SYSOUT=*
//ENTRADA  DD   DSN=BANCO.TRANSACOES.ENTRADA.D&LDATE,DISP=SHR
//VALIDADAS DD  DSN=BANCO.TRANSACOES.VALIDADAS.D&LDATE,
//              DISP=(NEW,CATLG,DELETE),
//              SPACE=(CYL,(50,10))
//REJEITADAS DD DSN=BANCO.TRANSACOES.REJEITADAS.D&LDATE,
//              DISP=(NEW,CATLG,DELETE),
//              SPACE=(CYL,(5,2))

//PROCESSA EXEC PGM=TXPROCESS
//SYSPRINT DD   SYSOUT=*
//VALIDTX  DD   DSN=BANCO.TRANSACOES.VALIDADAS.D&LDATE,DISP=SHR
//CONTAS   DD   DSN=BANCO.CADASTRO.CONTAS.CORRENTES,DISP=SHR
//SALDOS   DD   DSN=BANCO.SALDOS.ATUAIS,DISP=OLD
//EXTRATO  DD   DSN=BANCO.EXTRATOS.MOVIMENTO.D&LDATE,
//              DISP=(NEW,CATLG,DELETE),
//              SPACE=(CYL,(100,20))

//RELATOR  EXEC PGM=TXRELATORIO  
//SYSPRINT DD   SYSOUT=*
//MOVIMENTO DD  DSN=BANCO.EXTRATOS.MOVIMENTO.D&LDATE,DISP=SHR
//RESUMO   DD   DSN=BANCO.RELATORIOS.RESUMO.DIARIO.D&LDATE,
//              DISP=(NEW,CATLG,DELETE),
//              SPACE=(TRK,(50,10))
//REPORT   DD   SYSOUT=A
```

## Job de Conciliação Bancária

```jcl
//CONCILIA JOB (BANK002),'CONCILIACAO',CLASS=B,MSGCLASS=H
//STEP01   EXEC PGM=CONCILEXT
//SYSPRINT DD   SYSOUT=*
//EXTBANK  DD   DSN=BANCO.EXTRATOS.EXTERNOS.BACEN,DISP=SHR
//EXTINT   DD   DSN=BANCO.EXTRATOS.INTERNOS.CONSOLIDADO,DISP=SHR
//DIVERGE  DD   DSN=BANCO.CONCILIACAO.DIVERGENCIAS,
//              DISP=(NEW,CATLG,DELETE),
//              SPACE=(CYL,(10,3))

//STEP02   EXEC PGM=SORTUTIL
//SORTIN   DD   DSN=BANCO.CONCILIACAO.DIVERGENCIAS,DISP=SHR
//SORTOUT  DD   DSN=BANCO.CONCILIACAO.DIVERGENCIAS.SORTED,
//              DISP=(NEW,CATLG,DELETE),
//              SPACE=(CYL,(10,3))
//SYSIN    DD   *
  SORT FIELDS=(1,20,CH,A,21,8,ZD,A)
/*
```

## Job de Backup e Arquivamento

```jcl
//BACKUPTX JOB (BANK003),'BACKUP TRANSACOES',CLASS=C
//BACKUP01 EXEC PGM=ARQUIVTX
//SYSPRINT DD   SYSOUT=*
//ORIGEM   DD   DSN=BANCO.TRANSACOES.PROCESSADAS.D&LDATE,DISP=SHR
//DESTINO  DD   DSN=BANCO.ARQUIVO.TRANSACOES.M&LMONTH,
//              DISP=(MOD,CATLG,CATLG),
//              SPACE=(CYL,(200,50))

//BACKUP02 EXEC PGM=HSMDBACK
//ORIGINAL DD   DSN=BANCO.SALDOS.ATUAIS,DISP=SHR
//BACKUP   DD   DSN=BANCO.BACKUP.SALDOS.G0001V00,
//              DISP=(NEW,CATLG,DELETE),
//              SPACE=(CYL,(30,10))
//SYSIN    DD   DUMMY
```

## Descrição dos Programas

### TXVALIDA
- **Função**: Validação de transações bancárias
- **Input**: Transações de entrada diárias
- **Output**: Transações validadas e rejeitadas

### TXPROCESS  
- **Função**: Processamento principal das transações
- **Input**: Transações validadas, cadastro de contas
- **Output**: Saldos atualizados, extratos de movimento

### TXRELATORIO
- **Função**: Geração de relatórios de movimento
- **Input**: Extratos de movimento
- **Output**: Relatórios resumo e detalhados

### CONCILEXT
- **Função**: Conciliação entre extratos externos e internos
- **Input**: Extratos bancários BACEN e internos
- **Output**: Divergências encontradas

### ARQUIVTX
- **Função**: Arquivamento de transações processadas
- **Input**: Transações diárias processadas
- **Output**: Arquivo histórico mensal

Este sistema processa diariamente milhares de transações bancárias com validação, processamento e geração de relatórios gerenciais.
