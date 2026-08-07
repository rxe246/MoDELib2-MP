/* This file is part of MoDELib, the Mechanics Of Defects Evolution Library.
 *
 *
 * MoDELib is distributed without any warranty under the
 * GNU General Public License (GPL) v2 <http://www.gnu.org/licenses/>.
 */

#ifndef _model_DislocationMobilityBCC_cpp_
#define _model_DislocationMobilityBCC_cpp_

#include <numbers>
#include <cmath>
#include <string>
#include <filesystem>

#include <DislocationMobilityBCC.h>
#include <TextFileParser.h>

namespace model
{

    DislocationMobilityBCC::DislocationMobilityBCC(const double& b_SI,
                                                   const double& mu_SI,
                                                   const double& cs_SI,
                                                   const double& B0e_SI, const double& B1e_SI,
                                                   const double& B0s_SI, const double& B1s_SI,
                                                   const double& Bk_SI,
                                                   const double& dH0_SI,
                                                   const double& p_in,
                                                   const double& q_in,
                                                   const double& T0_in,
                                                   const double& tauC_in,
                                                   const double& a0_in,
                                                   const double& a1_in,
                                                   const double& a2_in,
                                                   const double& a3_in,
                                                   const double& dH0_SI_100,
                                                   const double& tauC_SI_100,
                                                   const double& a0_100_in,
                                                   const double& a1_100_in,
                                                   const double& a2_100_in,
                                                   const double& a3_100_in,
                                                   const MatrixDim& C2G_in) :
    /* init */ DislocationMobilityBase("BCC DislocationMobility"),
    /* init */ h(2.0*sqrt(2.0)/3.0), // units of b
    /* init */ w(25.0), // units of b
    /* init */ B0e(B0e_SI*cs_SI/(mu_SI*b_SI)),
    /* init */ B1e(B1e_SI*cs_SI/(mu_SI*b_SI)),
    /* init */ B0s(B0s_SI*cs_SI/(mu_SI*b_SI)),
    /* init */ B1s(B1s_SI*cs_SI/(mu_SI*b_SI)),
    /* init */ Bk(  Bk_SI*cs_SI/(mu_SI*b_SI)),
    /* init */ dH0(dH0_SI),
    /* init */ p(p_in),
    /* init */ q(q_in),
    /* init */ T0(T0_in),
    /* init */ tauC(tauC_in/mu_SI),
    /* init */ a0(a0_in),
    /* init */ a1(a1_in),
    /* init */ a2(a2_in),
    /* init */ a3(a3_in),
    /* init */ kB(kB_SI/mu_SI/std::pow(b_SI,3)),
    /* init */ theta_o1(14.0),
    /* init */ theta_o2(24.0),
    /* init */ theta_o3(24.0),
    /* init */ A_35(0.02298),
    /* init */ A_0(0.01454),
    /* init */ A_90(0.010),
    /* init */ dH0_100(dH0_SI_100),
    /* init */ tauC_100(tauC_SI_100/mu_SI),
    /* init */ a0_100(a0_100_in),
    /* init */ a1_100(a1_100_in),
    /* init */ a2_100(a2_100_in),
    /* init */ a3_100(a3_100_in),
    /* init */ C2G_matrix(C2G_in)
        {
            /*!*/
    }


    DislocationMobilityBCC::DislocationMobilityBCC(const PolycrystallineMaterialBase& material) :
    /* init */ DislocationMobilityBase("BCC mobility for "+material.materialName),
    /* init */ h(2.0*sqrt(2.0)/3.0), // units of b
    /* init */ w(25.0), // units of b
    /* init */ B0e(TextFileParser(material.materialFile).readScalar<double>("B0e_SI",true)*material.cs_SI/(material.mu_SI*material.b_SI)),
    /* init */ B1e(TextFileParser(material.materialFile).readScalar<double>("B1e_SI",true)*material.cs_SI/(material.mu_SI*material.b_SI)),
    /* init */ B0s(TextFileParser(material.materialFile).readScalar<double>("B0s_SI",true)*material.cs_SI/(material.mu_SI*material.b_SI)),
    /* init */ B1s(TextFileParser(material.materialFile).readScalar<double>("B1s_SI",true)*material.cs_SI/(material.mu_SI*material.b_SI)),
    /* init */ Bk (TextFileParser(material.materialFile).readScalar<double>("Bk_SI", true)*material.cs_SI/(material.mu_SI*material.b_SI)),
    /* init */ dH0(TextFileParser(material.materialFile).readScalar<double>("dH0_eV",true)),
    /* init */ p(TextFileParser(material.materialFile).readScalar<double>("p",true)),
    /* init */ q(TextFileParser(material.materialFile).readScalar<double>("q",true)),
    /* init */ T0(TextFileParser(material.materialFile).readScalar<double>("Tf",true)*material.Tm),
    /* init */ tauC(TextFileParser(material.materialFile).readScalar<double>("tauC_SI",true)/material.mu_SI),
    /* init */ a0(TextFileParser(material.materialFile).readScalar<double>("a0",true)),
    /* init */ a1(TextFileParser(material.materialFile).readScalar<double>("a1",true)),
    /* init */ a2(TextFileParser(material.materialFile).readScalar<double>("a2",true)),
    /* init */ a3(TextFileParser(material.materialFile).readScalar<double>("a3",true)),
    /* init */ kB(kB_SI/material.mu_SI/std::pow(material.b_SI,3)),
    /* init */ theta_o1(14.0),
    /* init */ theta_o2(24.0),
    /* init */ theta_o3(24.0),
    /* init */ A_35(0.02298),
    /* init */ A_0(0.01454),
    /* init */ A_90(0.010),
    /* init */ dH0_100(TextFileParser(material.materialFile).readScalar<double>("dH0_eV_100",true)),
    /* init */ tauC_100(TextFileParser(material.materialFile).readScalar<double>("tauC_SI_100",true)/material.mu_SI),
    /* init */ a0_100(TextFileParser(material.materialFile).readScalar<double>("a0_100",true)),
    /* init */ a1_100(TextFileParser(material.materialFile).readScalar<double>("a1_100",true)),
    /* init */ a2_100(TextFileParser(material.materialFile).readScalar<double>("a2_100",true)),
    /* init */ a3_100(TextFileParser(material.materialFile).readScalar<double>("a3_100",true))
        {
            try {
                /*!*/ std::filesystem::path materialPath(material.materialFile);
                /*!*/ std::string polycrystalFilePath = (materialPath.parent_path() / "polycrystal.txt").string();
                this->C2G_matrix = TextFileParser(polycrystalFilePath).readMatrix<double>("C2G1", 3, 3, true);
            } catch (const std::exception& e) {
                std::cerr << "Error initializing C2G_matrix in DislocationMobilityBCC: " << e.what() << std::endl;
            }
    }

    double DislocationMobilityBCC::sigmoid(const double & x)
    {
        return 2.0/(1.0+exp(2.0*x));
    }

    double DislocationMobilityBCC::velocity(const MatrixDim& S,
                                            const VectorDim& b,
                                            const VectorDim& xi,
                                            const VectorDim& n,
                                            const double& T)
    {
        return velocity(S,b,xi,n,T,0.0,0.0,nullptr);
    }

    double DislocationMobilityBCC::velocity(const MatrixDim& S,
                                            const VectorDim& b,
                                            const VectorDim& xi,
                                            const VectorDim& n,
                                            const double& T,
                                            const double& dL,
                                            const double& dt,
                                            const std::shared_ptr<StochasticForceGenerator>& sfg)
    {
        
        const double bNorm=b.norm();
        const VectorDim s = b/bNorm;
        const VectorDim n1 = Eigen::AngleAxisd(std::numbers::pi/3.0,s)*n;
        
        // Determine Dislocation Type
        bool isType100 = false;
        double tolerance = 1e-4; // Adjust tolerance if needed

        // Calculate Global-to-Crystal rotation matrix (using the member variable)
        MatrixDim G2C_matrix = C2G_matrix.inverse();

        // Transform s vector into Crystal Frame
        VectorDim s_crystal = G2C_matrix * s;

        // --- Check s_crystal components ---
        // Find the maximum absolute component in the crystal frame
        double max_abs_comp_crystal = std::max({std::fabs(s_crystal[0]), std::fabs(s_crystal[1]), std::fabs(s_crystal[2])});

        // Check <100> condition in Crystal Frame: Max comp near 1, others near 0
        if (std::fabs(max_abs_comp_crystal - 1.0) < tolerance) {
            double sum_abs_comps_crystal = std::fabs(s_crystal[0]) + std::fabs(s_crystal[1]) + std::fabs(s_crystal[2]);
            if (std::fabs(sum_abs_comps_crystal - max_abs_comp_crystal) < tolerance * 2) {
                isType100 = true;
            }
        }

        double vFinal;

        const double dg_approx = 0.0;
        const double sgm_approx = 0.5*sigmoid(-0.5*(0.05-dg_approx)/0.05);
        const double Bs_stoch = Bk*w/(2.0*h)*(1.0-sgm_approx)+(B0s+B1s*T)*sgm_approx;
        const double Be_stoch = B0e + B1e*T;

        if (isType100)
        {
            const double tau = s.transpose()*S*n;
            const double cos_theta = s.dot(xi);
            
            double thetaDeg = std::acos(cos_theta) * 180.0 / std::numbers::pi;
            double theta = thetaDeg;

            double V_0 = 0.010;
            double V_35 = 0.014;
            double V_54 = 0.005;
            double V_90 = 0.009;

            double w0 = 12.0;
            double w35 = 12.0;
            double w54 = 6.0;
            double w90 = 20.0;

            // --- 2. Calculate Dynamic Targets (Stress Scaled) ---
            double ref_stress = 1.0; 
            double stress_factor = std::fabs(tau) / ref_stress; 

            // Target Velocities (V_0, V_35, V_54, V_90)
            double V0  = V_0 * stress_factor;
            double V35 = V_35 * stress_factor;
            double V54 = V_54 * stress_factor; 
            double V90 = V_90 * stress_factor;

            const double M_inv[4][4] = {
            { 1.0000000305e+00, -1.7453231701e-04, 5.0300038867e-09, 9.5025368312e-08 },
            { -1.7453231698e-04, 1.0000021421e+00, -2.8819961526e-05, -5.6285298066e-04 },
            { 1.2786945960e-05, -7.3269638136e-02, 1.0000021116e+00, -4.4327283161e-02 },
            { 1.6516960212e-13, -9.4635743557e-10, 2.5418132780e-14, 1.0000000000e+00 },
            };


            double c0  = (M_inv[0][0] * V0) + (M_inv[0][1] * V35) + (M_inv[0][2] * V54) + (M_inv[0][3] * V90);           
            double c35 = (M_inv[1][0] * V0) + (M_inv[1][1] * V35) + (M_inv[1][2] * V54) + (M_inv[1][3] * V90);
            double c54 = (M_inv[2][0] * V0) + (M_inv[2][1] * V35) + (M_inv[2][2] * V54) + (M_inv[2][3] * V90);
            double c90 = (M_inv[3][0] * V0) + (M_inv[3][1] * V35) + (M_inv[3][2] * V54) + (M_inv[3][3] * V90);
            
            double g0 = c0 * (std::exp(-std::pow((theta - 0.0)/w0, 2)) + 
                            std::exp(-std::pow((theta - 180.0)/w0, 2)));

            double g35 = c35 * (std::exp(-std::pow((theta - 35.3)/w35, 2)) + 
                              std::exp(-std::pow((theta - 144.7)/w35, 2)));

            double g54 = c54 * (std::exp(-std::pow((theta - 54.7)/w54, 2)) + 
                              std::exp(-std::pow((theta - 125.3)/w54, 2)));

            double g90 = c90 * (std::exp(-std::pow((theta - 90.0)/w90, 2)));

            double vAnalytical = g0 + g35 + g54 + g90;
            vFinal = vAnalytical;

            if (sfg) {
                double B_avgStoch = (Bs_stoch + Be_stoch) / 2.0;
                vFinal += sfg->stochasticVelocity(kB, T, B_avgStoch, dL, dt);
            }
        }
        else
        {
            // Compute components of non-Schmid model
            const double tau=s.transpose()*S*n; // magnitude of resolved shear stress
            const double tauOrt=n.cross(s).transpose()*S*n;
            const double tau1=s.transpose()*S*n1; // resolved schear stress on
            const double tauOrt1=n1.cross(s).transpose()*S*n1;
            
            const double num=std::fabs(tau+a1*tau1);
            const double den=a0*tauC*sigmoid((a2*tauOrt+a3*tauOrt1)/a0/tauC);
            
            assert(den>0.0 && "den must be > 0.");
            
            const double Theta=num/den;
            const double dg = (Theta<1.0)? (std::pow(1.0-std::pow(Theta,p),q)-T/T0) : 0.0;
            const double dg1 = (dg>0.0)? dg : 0.0;
            const double expCoeff = exp(-dH0*dg1/(2.0*kB_eV*T));
            
            // Compute screw drag coeff
            const double sgm=0.5*sigmoid(-0.5*(0.05-dg1)/0.05);
            const double Bs=Bk*w/(2.0*h)*(1.0-sgm)+(B0s+B1s*T)*sgm; //kink-dominated to drag-dominated interpolation
            
            // Compute screw velocity
            double vs=std::fabs(tau)*bNorm/Bs*expCoeff;
            
            // Compute edge velocity
            double ve=std::fabs(tau)*bNorm/(B0e+B1e*T);
        
            if(sfg)
            {
                vs+=sfg->stochasticVelocity(kB,T,Bs,dL,dt);
                ve+=sfg->stochasticVelocity(kB,T,B0e+B1e*T,dL,dt);
            }
            
            // Interpolate ve and vs
            const double cos2=std::pow(s.dot(xi),2);
            vFinal = vs*cos2+ve*(1.0-cos2);
        }

        return vFinal;
    }


}
#endif
