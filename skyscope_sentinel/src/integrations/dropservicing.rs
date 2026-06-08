use std::collections::HashMap;

pub struct ServiceOpportunity {
    pub platform: String,
    pub job_id: String,
    pub description: String,
    pub budget: f64,
}

pub struct DropservicingSystem {
    pub categories: HashMap<String, Vec<String>>,
}

impl DropservicingSystem {
    pub fn new() -> Self {
        let mut categories = HashMap::new();
        categories.insert("AI Development".to_string(), vec!["python".to_string(), "openai".to_string()]);
        categories.insert("Web Automation".to_string(), vec!["playwright".to_string(), "rust".to_string()]);

        Self { categories }
    }

    pub async fn analyze_opportunity(&self, opp: ServiceOpportunity) -> bool {
        println!("Analyzing job {} on {}...", opp.job_id, opp.platform);

        for (category, skills) in &self.categories {
            for skill in skills {
                if opp.description.to_lowercase().contains(skill) {
                    println!("Matched category: {}. Proceeding with autonomous proposal...", category);
                    return true;
                }
            }
        }
        false
    }

    pub async fn submit_proposal(&self, job_id: &str, proposal: &str) {
        println!("Autonomous proposal submitted for job {}: {}", job_id, proposal);
    }
}
