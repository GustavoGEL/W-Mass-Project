source /cvmfs/lhcb.cern.ch/lib/etc/cern_profile.sh
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_100 x86_64-centos7-gcc10-opt

cd "just_pt_muon (Report)";
chmod u+x run_all.sh;
./run_all.sh;
cd ..;

cd "just_pt_muon (Summaries)";
chmod u+x run_all.sh;
./run_all.sh;
cd ..;

cd "pt_muon_regardless (Report)";
chmod u+x run_all.sh;
./run_all.sh;
cd ..;

cd "pt_muon_regardless (Summaries)";
chmod u+x run_all.sh;
./run_all.sh;
cd ..;

cd "pt_and_highest_photon (Report)";
chmod u+x run_all.sh;
./run_all.sh;
cd ..;

cd "pt_and_highest_photon (Summaries)";
chmod u+x run_all.sh;
./run_all.sh;
cd ..;

cd "pt_and_both_photons (Report)";
chmod u+x run_all.sh;
./run_all.sh;
cd ..;

cd "pt_and_both_photons (Summaries)";
chmod u+x run_all.sh;
./run_all.sh;
cd ..;
