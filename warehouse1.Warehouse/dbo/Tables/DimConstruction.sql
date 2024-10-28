CREATE TABLE [dbo].[DimConstruction] (

	[ConstructionID] int NULL, 
	[TypeConstruction] varchar(255) NULL
);


GO
ALTER TABLE [dbo].[DimConstruction] ADD CONSTRAINT UQ_b692288a_f471_45b7_89ba_11c416410186 unique NONCLUSTERED ([ConstructionID]);