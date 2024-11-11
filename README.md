# Scholexplorer-Dump-Processing-Libraries
<div style="text-align: center;">
    <img src="https://scholexplorer.openaire.eu/images/Logos/ScholeXplorer_logo.svg" alt="ScholeXplorer Logo" width="500"/>
</div>
<h1 style="text-align: center; ">Welcome to <a href="https://scholexplorer.openaire.eu/">Scholexplorer</a> Dump Processing Libraries!</h1>

This library is designed to process [Scholexplorer](https://scholexplorer.openaire.eu/) dumps and extract valuable insights from the data. 

Since its launch  [Scholexplorer](https://scholexplorer.openaire.eu/) has increased the number of Scholix relationships of two orders of magnitude, showing today an astonishing 5.5Bi entries. Its regular data dumps, published in Zenodo, reached the size of XXXX. As a consequence, the OpenAIRE team has decided to change the data storage strategy and format to ease its processing and reuse. The notebook in this repository includes scripts for processing the dump in order to:

- filter the relationships according to criteria such as provenance, semantics of relationships, and PID type;
- generate the Scholix records corresponsing to the filtered relationships.

The newly adopted dump format organizes the data into two distinct folders: __Entities__ and __Relationships__.



