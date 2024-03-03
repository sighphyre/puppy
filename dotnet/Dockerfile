ARG TAG=main

FROM mcr.microsoft.com/dotnet/sdk:6.0

RUN apt-get update && apt-get install -y git

WORKDIR /usr/src/base/unleash-client-dotnet

COPY ./unleash-client-dotnet .

# RUN git checkout $TAG
RUN dotnet restore src/Unleash/Unleash.csproj
RUN dotnet build src/Unleash/Unleash.csproj -c Release
RUN dotnet pack src/Unleash/Unleash.csproj -c Release -o ./nupkgs

WORKDIR /usr/src/base/harness

COPY ./harness/dotnet.csproj .
COPY ./harness/NuGet.Config .
COPY ./harness/Program.cs .

RUN dotnet restore dotnet.csproj
RUN dotnet build dotnet.csproj

CMD ["dotnet", "run"]
