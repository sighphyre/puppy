ARG TAG=main

FROM mcr.microsoft.com/dotnet/sdk:6.0

RUN apt-get update && apt-get install -y git

WORKDIR /usr/src/base/sdk

COPY ./dotnet .

# RUN git checkout $TAG
RUN dotnet restore src/Unleash/Unleash.csproj
RUN dotnet build src/Unleash/Unleash.csproj -c Release
RUN dotnet pack src/Unleash/Unleash.csproj -c Release -o ./nupkgs --no-build

WORKDIR /usr/src/base/harness

COPY ./scaffolds/dotnet/dotnet.csproj .
COPY ./scaffolds/dotnet/Program.cs .

RUN dotnet restore
RUN dotnet build

CMD ["dotnet", "run"]
