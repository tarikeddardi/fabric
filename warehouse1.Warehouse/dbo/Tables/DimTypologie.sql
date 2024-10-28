CREATE TABLE [dbo].[DimTypologie] (

	[TypologieID] int NULL, 
	[Typologie] varchar(255) NULL
);


GO
ALTER TABLE [dbo].[DimTypologie] ADD CONSTRAINT UQ_8bd88321_1bc2_4115_bf97_da1b8949b677 unique NONCLUSTERED ([TypologieID]);