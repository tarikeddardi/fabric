CREATE TABLE [dbo].[DimFinancement] (

	[FinancementID] int NULL, 
	[TypeFinancement] varchar(255) NULL
);


GO
ALTER TABLE [dbo].[DimFinancement] ADD CONSTRAINT UQ_27ed4456_7cc0_4630_8d40_107116aeb7af unique NONCLUSTERED ([FinancementID]);