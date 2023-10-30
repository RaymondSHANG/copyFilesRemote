#!/usr/bin/env nextflow

nextflow.enable.dsl=2
//RB10162_131_R2.fastq.gz
params.input_files = "/Volumes/MyRNASeqData/Hannah/RB10162/data/sample101_147/*{1,2}.fastq.gz"
//'smb://journal.medicine.arizona.edu/CIBS/Animal/OMICS/Data/RNASeq/Hannah/RB10162/data/sample101_147'
params.results_dir = "/Users/yshang/temp_share/sample101_147"

// A channel that contains a map with sample name and the file itself

file_channel = Channel.fromPath( params.input_files, checkIfExists: true )
                      .map { it -> [it.baseName, it] }


// An example process just head-ing the vcf
process CopyFilesRemote {

    publishDir("${params.results_dir}", mode: 'copy')

    input:
    tuple val(name), path(file_in)

    output:
    path("*_head.vcf")

    script:
    """ 
    cp $file_in ${name}.fastq.gz
    """

}        


workflow {
   CopyFilesRemote(file_channel)
}