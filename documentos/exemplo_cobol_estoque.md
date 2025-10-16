# Programa COBOL - Sistema de Controle de Estoque

Este documento descreve o programa COBOL para controle de estoque com procedures e copybooks.

## JCL de Execução

```jcl
//ESTOQUE  JOB (PROD123),'CONTROLE ESTOQUE',CLASS=B,MSGCLASS=H
//COMPILE  EXEC PGM=IGYCRCTL
//STEPLIB  DD   DSN=SYS1.COBOL.COMPILER,DISP=SHR
//SYSPRINT DD   SYSOUT=*
//SYSIN    DD   DSN=DESEN.COBOL.SOURCE(ESTOQUE01),DISP=SHR
//SYSLIN   DD   DSN=&&OBJSET,DISP=(NEW,PASS),
//              SPACE=(TRK,(10,5))

//LINKEDT  EXEC PGM=IEWL
//SYSLIB   DD   DSN=SYS1.COBOL.LINKLIB,DISP=SHR
//SYSLIN   DD   DSN=&&OBJSET,DISP=(OLD,DELETE)
//SYSLMOD  DD   DSN=PROD.LOADLIB(ESTOQUE01),DISP=SHR
//SYSPRINT DD   SYSOUT=*

//EXECPGM  EXEC PGM=ESTOQUE01
//STEPLIB  DD   DSN=PROD.LOADLIB,DISP=SHR
//SYSOUT   DD   SYSOUT=*
//PRODUTOS DD   DSN=EMPRESA.PRODUTOS.MASTER,DISP=SHR
//MOVTO    DD   DSN=EMPRESA.ESTOQUE.MOVIMENTOS,DISP=SHR
//RELEST   DD   DSN=EMPRESA.RELATORIOS.ESTOQUE.DIARIO,
//              DISP=(NEW,CATLG,DELETE),
//              SPACE=(CYL,(5,1))
```

## Stored Procedures Relacionadas

```jcl
//PROCEST  EXEC PGM=DB2BATCH
//SYSTSIN  DD   *
  CALL STORED-PROCEDURE-ESTOQUE-ATUALIZA(
    :WS-PRODUTO-ID,
    :WS-QUANTIDADE,
    :WS-TIPO-MOVIMENTO
  )
  CALL STORED-PROCEDURE-ESTOQUE-CONSULTA(
    :WS-PRODUTO-ID,
    :WS-SALDO-ATUAL
  )
/*
//DATABASE DD   DSN=EMPRESA.DB2.ESTOQUE.TABELAS,DISP=SHR
//SYSPRINT DD   SYSOUT=*
```

## Batch de Backup

```jcl
//BACKUP   EXEC PGM=IEBGENER
//SYSPRINT DD   SYSOUT=*
//SYSUT1   DD   DSN=EMPRESA.PRODUTOS.MASTER,DISP=SHR
//SYSUT2   DD   DSN=EMPRESA.BACKUP.PRODUTOS.G0001V00,
//              DISP=(NEW,CATLG,DELETE),
//              SPACE=(CYL,(20,5))
//SYSIN    DD   DUMMY
```

## Descrição dos Programas

### ESTOQUE01
- **Função**: Programa principal de controle de estoque
- **Linguagem**: COBOL
- **Datasets**: Produtos master, movimentos, relatórios

### Procedures DB2
- **STORED-PROCEDURE-ESTOQUE-ATUALIZA**: Atualiza saldos no banco
- **STORED-PROCEDURE-ESTOQUE-CONSULTA**: Consulta saldos atuais

Este sistema processa movimentações de estoque e gera relatórios diários de posição.
