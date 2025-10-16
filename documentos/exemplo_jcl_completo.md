# JCL Exemplo Completo - Sistema de Folha de Pagamento

Este documento descreve um job JCL completo para processamento de folha de pagamento com múltiplos steps.

## Job Principal - FOLHAPGTO

```jcl
//FOLHAPGTO JOB (ACCT001),'FOLHA PAGAMENTO',CLASS=A,MSGCLASS=X
//STEP001  EXEC PGM=VALIDFUNC
//SYSPRINT DD   SYSOUT=*
//ENTRADA  DD   DSN=EMPRESA.FUNCIONARIOS.DADOS,DISP=SHR
//SAIDA    DD   DSN=EMPRESA.FUNCIONARIOS.VALIDADOS,
//              DISP=(NEW,CATLG,DELETE),
//              SPACE=(CYL,(5,1)),
//              DCB=(RECFM=FB,LRECL=80,BLKSIZE=8000)

//STEP002  EXEC PGM=CALCSAL01
//STEPLIB  DD   DSN=PROD.COBOL.LOADLIB,DISP=SHR
//SYSPRINT DD   SYSOUT=*
//FUNCVAL  DD   DSN=EMPRESA.FUNCIONARIOS.VALIDADOS,DISP=SHR
//TABSAL   DD   DSN=EMPRESA.TABELAS.SALARIOS,DISP=SHR
//RELSAL   DD   DSN=EMPRESA.RELATORIOS.SALARIOS,
//              DISP=(NEW,CATLG,DELETE),
//              SPACE=(CYL,(10,2))

//STEP003  EXEC PGM=GERAIMPOSTO
//SYSPRINT DD   SYSOUT=*
//ENTRADA  DD   DSN=EMPRESA.RELATORIOS.SALARIOS,DISP=SHR
//TABIR    DD   DSN=EMPRESA.TABELAS.IMPOSTOS.RENDA,DISP=SHR
//SAIDIMP  DD   DSN=EMPRESA.IMPOSTOS.CALCULADOS,
//              DISP=(NEW,CATLG,DELETE),
//              SPACE=(TRK,(100,10))
```

## Descrição dos Steps

### STEP001 - Validação de Funcionários
- **Programa**: VALIDFUNC
- **Função**: Valida dados dos funcionários antes do processamento
- **Input**: EMPRESA.FUNCIONARIOS.DADOS
- **Output**: EMPRESA.FUNCIONARIOS.VALIDADOS

### STEP002 - Cálculo de Salários  
- **Programa**: CALCSAL01
- **Função**: Calcula salários base dos funcionários
- **Input**: EMPRESA.FUNCIONARIOS.VALIDADOS, EMPRESA.TABELAS.SALARIOS
- **Output**: EMPRESA.RELATORIOS.SALARIOS

### STEP003 - Geração de Impostos
- **Programa**: GERAIMPOSTO
- **Função**: Calcula impostos sobre os salários
- **Input**: EMPRESA.RELATORIOS.SALARIOS, EMPRESA.TABELAS.IMPOSTOS.RENDA
- **Output**: EMPRESA.IMPOSTOS.CALCULADOS

Este job processa a folha de pagamento em 3 etapas sequenciais, validando dados, calculando salários e gerando relatórios de impostos.
