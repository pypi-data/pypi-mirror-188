from dataclasses import dataclass
from prettytable import PrettyTable
from scipy import stats
from tabulate import tabulate

@dataclass(frozen=True)
class Test:
    a: str
    b: int
    c: float = None
    

@dataclass(frozen=True)
class ModelComparisonResult:
    comparison: str
    df: int
    statistic: float
    pvalue: float
    
    def __str__(self):
        x = [(k, v) for k, v in self.__dict__.items()]
        return str(table(x, headers=['', 'performance']))

@dataclass(frozen=True)
class PerformanceData:
    TPR: float
    FPR: float
    dprime: float
    aprime: float
    cbias: float
    beta: float
    Az: float
    AUC: float
    
    def __repr__(self):
        x = [(k, v) for k, v in self.__dict__.items()]
        return str(table(x, headers=['', 'performance']))

@dataclass(eq=False, frozen=True)
class FitResults:
    model: str
    success: bool
    # method: str
    # statistic: float
    X2: float
    G: float
    LL: float
    AIC: float
    BIC: float
    SSE: float
    
    def __repr__(self):
        x = [(k, v) for k, v in self.__dict__.items()]
        return str(table(x, headers=['', 'fit results']))


if __name__ == '__main__':
    comparison = ModelComparisonResult('G(EVSD - DPSD)', 1, 58.059846726081204, 2.542635548e-14)

    dpsd_performance = PerformanceData(
        TPR = 0.7051835853131749,
        FPR = 0.2911849710982659,
        dprime = 1.0892944588577766,
        aprime = 0.7927876595351733,
        cbias = 0.005279044808288003,
        beta = 1.0057669997424947,
        Az = 0.7598372495902206,
        AUC = 0.7439343243677308
    )
    evsd_performance = PerformanceData(
        TPR = 0.7051835853131749,
        FPR = 0.2911849710982659,
        dprime = 1.0892944588577766,
        aprime = 0.7927876595351733,
        cbias =  0.005279044808288003,
        beta = 1.0057669997424947,
        Az = 0.7598372495902206,
        AUC = 0.7439343243677308
    )
    
    dpsd_results = FitResults(
        'Dual Process Signal Detection',
        True,
        # 'G',
        # 23.17123943644981,
        23.71810819195668,
        23.171239436451515,
        -8692.438373467647,
        17398.876746935293,
        17441.92598074611,
        0.004341720323097594
    )
    
    print(dpsd_performance)