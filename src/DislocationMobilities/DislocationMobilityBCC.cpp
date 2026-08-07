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
#include <vector>
#include <iostream>

#include <DislocationMobilityBCC.h>
#include <TextFileParser.h>

namespace model
{
    static bool solve_5x5(double A[5][5], double b[5], double x[5]) {
        const int N = 5;
        for (int i = 0; i < N; i++) {
            double maxEl = std::abs(A[i][i]);
            int maxRow = i;
            for (int k = i + 1; k < N; k++) {
                if (std::abs(A[k][i]) > maxEl) { maxEl = std::abs(A[k][i]); maxRow = k; }
            }
            if (maxEl < 1e-12) return false; 
            for (int k = i; k < N; k++) std::swap(A[maxRow][k], A[i][k]);
            std::swap(b[maxRow], b[i]);
            for (int k = i + 1; k < N; k++) {
                double c = -A[k][i] / A[i][i];
                for (int j = i; j < N; j++) {
                    if (i == j) A[k][j] = 0; else A[k][j] += c * A[i][j];
                }
                b[k] += c * b[i];
            }
        }
        for (int i = N - 1; i >= 0; i--) {
            double sum = 0;
            for (int j = i + 1; j < N; j++) sum += A[i][j] * x[j];
            x[i] = (b[i] - sum) / A[i][i];
        }
        return true;
    }

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
                                                   const double& tauC_SI_100,
                                                   const double& a0_100_in,
                                                   const double& a1_100_in,
                                                   const double& a2_100_in,
                                                   const double& a3_100_in,
                                                   const double& dH0_0_100_in,
                                                   const double& dH0_35_100_in,
                                                   const double& dH0_54_100_in,
                                                   const double& dH0_90_100_in,
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
    /* init */ tauC_100(tauC_SI_100/mu_SI),
    /* init */ a0_100(a0_100_in),
    /* init */ a1_100(a1_100_in),
    /* init */ a2_100(a2_100_in),
    /* init */ a3_100(a3_100_in),
    /* init */ dH0_0_100(dH0_0_100_in),
    /* init */ dH0_35_100(dH0_35_100_in),
    /* init */ dH0_54_100(dH0_54_100_in),
    /* init */ dH0_90_100(dH0_90_100_in),
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
    /* init */ tauC_100(TextFileParser(material.materialFile).readScalar<double>("tauC_SI_100",true)/material.mu_SI),
    /* init */ a0_100(TextFileParser(material.materialFile).readScalar<double>("a0_100",true)),
    /* init */ a1_100(TextFileParser(material.materialFile).readScalar<double>("a1_100",true)),
    /* init */ a2_100(TextFileParser(material.materialFile).readScalar<double>("a2_100",true)),
    /* init */ a3_100(TextFileParser(material.materialFile).readScalar<double>("a3_100",true)),
    /* init */ dH0_0_100(TextFileParser(material.materialFile).readScalar<double>("dH0_0_100",true)),
    /* init */ dH0_35_100(TextFileParser(material.materialFile).readScalar<double>("dH0_35_100",true)),
    /* init */ dH0_54_100(TextFileParser(material.materialFile).readScalar<double>("dH0_54_100",true)),
    /* init */ dH0_90_100(TextFileParser(material.materialFile).readScalar<double>("dH0_90_100",true))
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

        if (isType100)
        {

            const double tau = s.transpose()*S*n; 
            double cos_theta = s.dot(xi);
            if (cos_theta > 1.0) cos_theta = 1.0;
            if (cos_theta < -1.0) cos_theta = -1.0; 
            const double thetaRad = std::acos(cos_theta);

            const VectorDim n1 = Eigen::AngleAxisd(std::numbers::pi/2.0,s)*n;
            
            const double dH0_vals[4] = {dH0_0_100, dH0_35_100, dH0_54_100, dH0_90_100};

            const double tauOrt = n.cross(s).transpose()*S*n;
            const double tau1 = s.transpose()*S*n1; 
            const double tauOrt1 = n1.cross(s).transpose()*S*n1;

            const double num=std::fabs(tau+a1_100*tau1);
            const double den=a0_100*tauC_100*sigmoid((a2_100*tauOrt+a3_100*tauOrt1)/a0_100/tauC_100);
            
            assert(den>0.0 && "den must be > 0.");
            
            const double Theta=num/den;
            const double dg = (Theta<1.0)? (std::pow(1.0-std::pow(Theta,p),q)-T/T0) : 0.0;
            const double dg1 = (dg>0.0)? dg : 0.0;
            const double sgm=0.5*sigmoid(-0.5*(0.05-dg1)/0.05);
            const double Bs=Bk*w/(2.0*h)*(1.0-sgm)+(B0s+B1s*T)*sgm; //kink-dominated to drag-dominated interpolation

            // Target Velocities (V_0, V_35, V_54, V_90)
            double v_targ[4];
            for(int i=0; i<4; ++i) {
                double B_val = (i==3) ? (B0e+B1e*T) : (Bs); // From W.txt
                
                double dG = dH0_vals[i] * dg1;
                if (dG < 0) dG = 0.0;

                double pre_factor = (std::fabs(tau) * bNorm) / B_val;
                v_targ[i] = pre_factor * std::exp(-dG / (2.0 * kB_eV * T));
            }

            double A[5][5];
            double b_vec[5];
            double angs[4] = {0.0, 35.3, 54.7, 90.0};
            
            for(int i=0; i<4; ++i) {
                b_vec[i] = v_targ[i]; // RHS is the target velocity
                double th = angs[i] * std::numbers::pi / 180.0;
                for(int n=0; n<5; ++n) {
                    A[i][n] = std::cos(2.0 * n * th);
                }
            }
            
            double th_dip = 54.7 * std::numbers::pi / 180.0;
            b_vec[4] = 0.0;
            A[4][0] = 0.0;
            for(int n=1; n<5; ++n) {
                A[4][n] = -2.0 * n * std::sin(2.0 * n * th_dip);
            }

            double c[5]; 
            if(solve_5x5(A, b_vec, c)) {
                // Sum the Fourier Series
                vFinal = 0.0;
                for(int n=0; n<5; ++n) {
                    vFinal += c[n] * std::cos(2.0 * n * thetaRad);
                }
            } else {
                // Fallback if matrix is singular (rare)
                vFinal = v_targ[0]; 
            }

            if (sfg) {
                double B_avg = (B0e+B1e*T + Bs) / 2.0;
                vFinal += sfg->stochasticVelocity(kB, T, B_avg, dL, dt);
            }

            return vFinal;
        }
        else
        {
            // Compute components of non-Schmid model
            const double tau=s.transpose()*S*n; // magnitude of resolved shear stress
            const double tauOrt=n.cross(s).transpose()*S*n;
            const VectorDim n1 = Eigen::AngleAxisd(std::numbers::pi/3.0,s)*n;
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
