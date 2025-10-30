
open import Data.Nat using (ℕ; _+_; _*_; zero; suc)
open import Data.Vec using (Vec; []; _∷_; tabulate; lookup; foldr; map)
open import Data.Float using (Float; _+_; _*_)
open import Data.Fin using (Fin; fromℕ; toℕ)

module ErsatzLA where

    data Space : Set where
       coord : (dim : ℕ) → Space

    data Matrix : (rows cols : ℕ) → Set where
        mkMatrix : {rows cols : ℕ} → (dat : Vec Float (rows * cols)) → Matrix rows cols

    get : {rows cols : ℕ} → Matrix rows cols → Fin rows → Fin cols → Float
    get {rows} {cols} (mkMatrix dat) i j = lookup dat (fromℕ (toℕ i * cols + toℕ j))

    data LinearMap : (U V : Space) → Set where
        asMatrix : {rows cols : ℕ} 
                 → (matrixData : Vec Float (rows * cols)) 
                 → LinearMap (coord rows) (coord cols)

    -- Helper function to create identity matrix data (simplified)
    identityMatrix : (n : ℕ) → Vec Float (n * n)
    identityMatrix n = tabulate (λ i → 1.0) -- Simplified for now
    
    identity : (U : Space) → LinearMap U U
    identity (coord n) = asMatrix (identityMatrix n)

    -- Matrix multiplication for flattened matrices
    composeMatrices : {rows mid cols : ℕ} 
                    → Vec Float (rows * mid) 
                    → Vec Float (mid * cols) 
                    → Vec Float (rows * cols)
    composeMatrices {rows} {mid} {cols} A B = 
        tabulate (λ (i,j) → foldr (Data.Float._+_) 0.0 (map (λ k → A !! (i * mid + k) * B !! (k * cols + j)) (fin 0 (mid - 1))))

    compose : {U V W : Space} → LinearMap U V → LinearMap V W → LinearMap U W
    compose (asMatrix F) (asMatrix G) = asMatrix (composeMatrices F G)