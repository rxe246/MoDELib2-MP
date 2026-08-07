/* This file is part of MoDELib, the Mechanics Of Defects Evolution Library.
 *
 *
 * MoDELib is distributed without any warranty under the
 * GNU General Public License (GPL) v2 <http://www.gnu.org/licenses/>.
 */

#ifndef _model_DislocationMobilityBCC100_h_
#define _model_DislocationMobilityBCC100_h_

#include <DislocationMobilityBase.h>

namespace model
{
    struct DislocationMobilityBCC100 : public DislocationMobilityBase
    {
        
        typedef Eigen::Matrix<double,3,3> MatrixDim;
        typedef Eigen::Matrix<double,3,1> VectorDim;
        
        
        static constexpr double kB_eV=8.617e-5;       // Boltzmann constant in [eV]
        static constexpr double kB_SI=1.38064852e-23; // Boltzmann constant in SI units [J/K]
        
        const double h;
        const double w;
        const double B0e;
        const double B1e;
        const double B0s;
        const double B1s;
        const double Bk;
        const double p;
        const double q;
        const double T0;
        const double tauC_100;
        const double a0_100;
        const double a1_100;
        const double a2_100;
        const double a3_100;
        const double dH0_0_100;
        const double dH0_35_100;
        const double dH0_54_100;
        const double dH0_90_100;
        const double kB;
        
        DislocationMobilityBCC100(const double& b_SI,
                            const double& mu_SI,
                            const double& cs_SI,
                            const double& B0e_SI, const double& B1e_SI,
                            const double& B0s_SI, const double& B1s_SI,
                            const double& Bk_SI,
                            const double& p_in,
                            const double& q_in,
                            const double& T0_in,
                            const double& tauC_in_100,
                            const double& a0_100_in,
                            const double& a1_100_in,
                            const double& a2_100_in,
                            const double& a3_100_in,
                            const double& dH0_0_100_in,
                            const double& dH0_35_100_in,
                            const double& dH0_54_100_in,
                            const double& dH0_90_100_in) ;
        
        DislocationMobilityBCC100(const PolycrystallineMaterialBase& material) ;
        
        static double sigmoid(const double & x);
        
        double velocity(const MatrixDim& S,
                        const VectorDim& b,
                        const VectorDim& xi,
                        const VectorDim& n,
                        const double& T,
                        const double& dL,
                        const double& dt,
                        const std::shared_ptr<StochasticForceGenerator>& sfg) ;
        
        double velocity(const MatrixDim& S,
                        const VectorDim& b,
                        const VectorDim& xi,
                        const VectorDim& n,
                        const double& T) ;
        
    };
    
}
#endif
